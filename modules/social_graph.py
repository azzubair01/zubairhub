import networkx as nx
import pandas as pd
import streamlit as st
import plotly.graph_objects as go

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
        st.rerun()

    # Display in table
    edited_df = st.data_editor(
        family_df,
        num_rows="dynamic",
        use_container_width=True,
        column_config={
            "Name": st.column_config.TextColumn("Name", required=True),
            "Parent": st.column_config.TextColumn("Parent", required=True),
            "Relationship": st.column_config.SelectboxColumn("Relationship", options=["Son", "Daughter"]),
        },
        key="family_editor"
    )

    if not edited_df.equals(family_df):
        edited_df.to_excel('modules/azzubair_family.xlsx', index=False)
        st.rerun()

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
