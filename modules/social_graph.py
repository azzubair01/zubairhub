import networkx as nx
import pandas as pd
import streamlit as st
from st_aggrid.grid_options_builder import GridOptionsBuilder
from st_aggrid import AgGrid, GridUpdateMode
import plotly.graph_objects as go
import plotly.express as px


def _display_header():
    text = "<h1 style='text-align: center; color: var(--text-color);'> \
                  👨‍👩‍👧‍👦 Azzubair's Family Graph!</h1>"
    st.markdown(text, unsafe_allow_html=True)
    st.write("---")


def _get_family_data():
    return pd.read_excel('modules/azzubair_family.xlsx')


def _render_input_form(family_df):
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
    return family_df


def _render_aggrid_table(family_df):
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
                family_df = family_df[~family_df.index.isin(sel_row_list)]
                family_df.to_excel('modules/azzubair_family.xlsx', index=False)
    return family_df


def _generate_and_display_graph(family_df):
    if not family_df.empty:
        G = nx.from_pandas_edgelist(family_df, source='Parent', target='Name', create_using=nx.Graph())
        # Generate the layout
        pos = nx.spring_layout(G)

        # Extract node and edge information for Plotly
        edge_x = []
        edge_y = []
        for edge in G.edges():
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            edge_x.append(x0)
            edge_x.append(x1)
            edge_x.append(None)
            edge_y.append(y0)
            edge_y.append(y1)
            edge_y.append(None)

        edge_trace = go.Scatter(
            x=edge_x, y=edge_y,
            line=dict(width=0.5, color='#888'),
            hoverinfo='none',
            mode='lines')

        node_x = []
        node_y = []
        node_text = []
        node_colors = []

        # Identify children of Azeman or Kartinah
        azeman_kartinah_children = family_df[
            (family_df['Parent'] == 'AZEMAN') | (family_df['Parent'] == 'KARTINAH')
        ]['Name'].tolist()

        # Identify Kartinah and her parents for pink coloring
        kartinah_relatives_for_pink = []
        if 'KARTINAH' in family_df['Name'].values:
            kartinah_relatives_for_pink.append('KARTINAH')
            # Check if Kartinah has a parent in the dataframe
            kartinah_parents = family_df[family_df['Name'] == 'KARTINAH']['Parent'].tolist()
            if kartinah_parents:
                kartinah_relatives_for_pink.extend(kartinah_parents)


        for node in G.nodes():
            x, y = pos[node]
            node_x.append(x)
            node_y.append(y)
            node_text.append(node)
            # Assign color based on whether the node is a child of Azeman or Kartinah
            if node in azeman_kartinah_children:
                node_colors.append('green')
            elif node in kartinah_relatives_for_pink:
                node_colors.append('pink')
            else:
                node_colors.append('#888') # Default color

        node_trace = go.Scatter(
            x=node_x, y=node_y,
            mode='markers+text',
            hoverinfo='text',
            marker=dict(
                showscale=False,
                size=10,
                color=node_colors, # Use the list of colors
                line_width=2),
            text=node_text,
            textposition="top center"
        )

        fig = go.Figure(data=[edge_trace, node_trace],
                        layout=go.Layout(
                            titlefont_size=16,
                            showlegend=False,
                            hovermode='closest',
                            margin=dict(b=20, l=5, r=5, t=40),
                            annotations=[dict(
                                text="",
                                showarrow=False,
                                xref="paper", yref="paper",
                                x=0.005, y=-0.002)],
                            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                        )

        fig.update_layout(height=550, width=600)
        st.plotly_chart(fig, width='stretch')


@st.fragment
def family_graph():
    _display_header()
    family_df = _get_family_data()
    family_df = _render_input_form(family_df)
    family_df = _render_aggrid_table(family_df)
    _generate_and_display_graph(family_df)
