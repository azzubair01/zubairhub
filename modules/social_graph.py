import networkx as nx
import pandas as pd
import streamlit as st
import plotly.graph_objects as go
from st_aggrid.grid_options_builder import GridOptionsBuilder
from st_aggrid import AgGrid, GridUpdateMode

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
        new_row = pd.DataFrame({'Name': name, 'Parent': parent, 'Relationship': relationship}, index=[index])
        family_df = pd.concat([family_df, new_row])
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

    sel_row_df = pd.DataFrame(grid_table["selected_rows"])

    if not sel_row_df.empty:
        # Assuming the structure of selected_rows based on previous code
        sel_row_list = sel_row_df['_selectedRowNodeInfo'].apply(lambda x: x['nodeRowIndex']).tolist()
        col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
        with col4:
            button_delete = st.button('Delete')
            if button_delete:
                df_delete = family_df[~family_df.index.isin(sel_row_list)]
                df_delete.to_excel('modules/azzubair_family.xlsx', index=False)

    if not family_df.empty:

        G = nx.from_pandas_edgelist(family_df, source='Name', target='Parent', edge_attr=True)

        pos = nx.spring_layout(G)

        edge_x = []
        edge_y = []
        for edge in G.edges():
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            edge_x.extend([x0, x1, None])
            edge_y.extend([y0, y1, None])

        edge_trace = go.Scatter(
            x=edge_x, y=edge_y,
            line=dict(width=0.5, color='#888'),
            hoverinfo='none',
            mode='lines')

        node_x = []
        node_y = []
        node_text = []
        for node in G.nodes():
            x, y = pos[node]
            node_x.append(x)
            node_y.append(y)
            node_text.append(node)

        node_trace = go.Scatter(
            x=node_x, y=node_y,
            mode='markers+text',
            hoverinfo='text',
            text=node_text,
            textposition="top center",
            marker=dict(
                showscale=False,
                color='lightblue',
                size=10,
                line_width=2))

        fig = go.Figure(data=[edge_trace, node_trace],
                        layout=go.Layout(
                            showlegend=False,
                            hovermode='closest',
                            margin=dict(b=0, l=0, r=0, t=0),
                            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                        )

        st.plotly_chart(fig, width="stretch")
