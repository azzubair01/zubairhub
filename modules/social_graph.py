import networkx as nx
import pandas as pd
import streamlit as st
from st_aggrid.grid_options_builder import GridOptionsBuilder
from st_aggrid import AgGrid, GridUpdateMode
from bokeh.plotting import Figure, from_networkx
from bokeh.palettes import Spectral4
from bokeh.layouts import gridplot
from bokeh.models import ColumnDataSource, LabelSet, BoxSelectTool, Circle, HoverTool, MultiLine, NodesAndLinkedEdges, \
    Range1d
from bokeh.models.tools import TapTool, PanTool, WheelZoomTool, SaveTool, ResetTool


@st.fragment
def family_graph():
    text = "<h1 style='text-align: center; color: var(--text-color);'>\
                  👨‍👩‍👧‍👦 Azzubair's Family Graph!</h1>"

    st.markdown(text, unsafe_allow_html=True)
    st.write("---")
    family_df = pd.read_excel('modules/azzubair_family.xlsx')

    col1, col2, col3 = st.columns(3)

    with col1:
        name = st.text_input('Name: ').upper()

    with col2:
        parent = st.text_input('Parent: ').upper()

    with col3:
        relationship = st.selectbox('Relationship: ', ['Son', 'Daughter'])

    col1, col2, col3, col4, col5 = st.columns(5)

    with col3:
        update_button = st.button('Update table')

    if update_button:
        index = len(family_df)
        family_df = family_df.append(
            pd.DataFrame({'Name': name, 'Parent': parent, 'Relationship': relationship}, index=[index]))
        family_df.to_excel('modules/azzubair_family.xlsx', index=False)

    # Display in table
    gd = GridOptionsBuilder.from_dataframe(family_df)
    gd.configure_pagination(enabled=True, paginationAutoPageSize=False, paginationPageSize=10)
    gd.configure_selection(selection_mode='multiple', use_checkbox=True)
    gd.configure_default_column(editable=True, groupable=True, sorteable=True, filterable=True)
    grid_options = gd.build()

    grid_table = AgGrid(
        family_df,
        gridOptions=grid_options,
        update_mode=GridUpdateMode.SELECTION_CHANGED,
        fit_columns_on_grid_load=True,
        theme="alpine")

    sel_row_df = pd.DataFrame(grid_table["selected_rows"]).iloc[:, :1]

    if not sel_row_df.empty:
        sel_row_df = pd.DataFrame(grid_table["selected_rows"]).iloc[:, :1]
        sel_row_df['index'] = sel_row_df['_selectedRowNodeInfo'].apply(lambda x: x['nodeRowIndex'])
        sel_row_list = sel_row_df['index'].tolist()
        col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
        with col4:
            button_delete = st.button('Delete')
            if button_delete:
                df_delete = family_df[~family_df.index.isin(sel_row_list)]
                df_delete.to_excel('modules/azzubair_family.xlsx', index=False)

    if not family_df.empty:

        G = nx.from_pandas_edgelist(family_df, source='Name', target='Parent', edge_attr=True)

        # Generate the layout and set the 'pos' attribute
        pos = nx.drawing.layout.spring_layout(G)
        nx.set_node_attributes(G, pos, 'pos')

        edge_x = []
        edge_y = []
        for edge in G.edges():
            x0, y0 = G.nodes[edge[0]]['pos']
            x1, y1 = G.nodes[edge[1]]['pos']
            edge_x.append(x0)
            edge_x.append(x1)
            edge_x.append(None)
            edge_y.append(y0)
            edge_y.append(y1)
            edge_y.append(None)

        graph_renderer = from_networkx(G, layout_function=nx.spring_layout)
        plot = Figure(height=550, width=600, tools="pan,wheel_zoom,save,reset", active_scroll='wheel_zoom',
                      x_range=Range1d(-1.1, 1.1), y_range=Range1d(-1.1, 1.1), title='')
        plot.title.text = ""
        graph_renderer.node_renderer.glyph = Circle(radius=0.01, fill_color=Spectral4[3])
        graph_renderer.node_renderer.selection_glyph = Circle(radius=0.01, fill_color=Spectral4[2])
        graph_renderer.node_renderer.hover_glyph = Circle(radius=0.01, fill_color=Spectral4[1])
        graph_renderer.edge_renderer.glyph = MultiLine(line_color="lightblue", line_width="edge_width", )
        graph_renderer.edge_renderer.selection_glyph = MultiLine(line_color=Spectral4[2], line_width="edge_width")
        graph_renderer.edge_renderer.hover_glyph = MultiLine(line_color=Spectral4[1], line_width="edge_width")
        graph_renderer.selection_policy = NodesAndLinkedEdges()
        graph_renderer.inspection_policy = NodesAndLinkedEdges()
        HOVER_TOOLTIPS = [("Item", "@index")]
        plot.add_tools(HoverTool(tooltips=HOVER_TOOLTIPS), WheelZoomTool(), TapTool(), BoxSelectTool(), PanTool(),
                       SaveTool(), ResetTool())
        plot.renderers.append(graph_renderer)
        x, y = zip(*graph_renderer.layout_provider.graph_layout.values())
        node_labels = list(graph_renderer.layout_provider.graph_layout.keys())
        source = ColumnDataSource({'x': x, 'y': y,
                                   'item': [node_labels[i] for i in range(len(x))]})
        labels = LabelSet(x='x', y='y', text='item', source=source,
                          background_fill_color='white', text_font_size='10px')
        plot.renderers.append(labels)
        # plot.outline_line_color = None
        # plot.xgrid.grid_line_color = None
        # plot.ygrid.grid_line_color = None
        # plot.axis.visible = False
        #
        # # Plot network graph
        st.bokeh_chart(gridplot([[plot]], sizing_mode='stretch_width'), use_container_width=True)
