import pandas as pd
from pathlib import Path
import random
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.express as px

categories = ['Baseline', 'On_treatment', 'Surgery', 'Relapse']

df_combined = pd.DataFrame(
    columns=['patient_id', 'Timepoint', 'mutations', 'silent mutations', 'nonsilent mutations', 'heavy', 'patient_count', 'cancer'])

for cancer in ["PBMC_DDLPS", "PBMC_UPS", "tumor_DDLPS", "tumor_UPS"]:
    meta = pd.read_csv(
        f"/rsrch4/home/mol_cgenesis/EMC_BIC_rsrch4/nkdang/Sarcoma_Project/meta/{cancer}.csv").astype({"patient_id": str})
    mutation = pd.read_csv(f"/rsrch4/home/mol_cgenesis/EMC_BIC_rsrch4/nkdang/Sarcoma_Project/IMGT/{cancer}/8_V-REGION-nt-mutation-statistics.txt", sep='\t', index_col=0)[
        ['Sequence ID', 'V-REGION Nb of mutations', 'V-REGION Nb of silent mutations', 'V-REGION Nb of nonsilent mutations', 'V-DOMAIN Functionality']]
    df_cluster = pd.DataFrame(
        columns=['patient_id', 'Timepoint', 'mutations', 'silent mutations', 'nonsilent mutations', 'heavy', 'patient_count'])

    for cluster_path in Path(f"/rsrch4/home/mol_cgenesis/EMC_BIC_rsrch4/nkdang/Sarcoma_Project/results/{cancer}/heavy/clustering_convergence/clusters").glob("**/*.csv"):
        cluster = pd.read_csv(cluster_path)[['sample_id', 'Sequence ID']]

        assert cluster['Sequence ID'].is_unique == True
        cluster = cluster.merge(mutation, how='left',
                                left_on="Sequence ID", right_on="Sequence ID")

        assert meta['sample_id'].is_unique == True
        cluster = cluster.merge(meta[['patient_id', 'sample_id', 'Timepoint']], how='left',
                                left_on="sample_id", right_on="sample_id")

        cluster['mutations'] = cluster['V-REGION Nb of mutations'].apply(lambda x: int(
            str(x)[:str(x).find("(")]) if str(x).find("(") != -1 else x)
        cluster['silent mutations'] = cluster['V-REGION Nb of silent mutations'].apply(
            lambda x: int(str(x)[:str(x).find("(")]) if str(x).find("(") != -1 else x)
        cluster['nonsilent mutations'] = cluster['V-REGION Nb of nonsilent mutations'].apply(
            lambda x: int(str(x)[:str(x).find("(")]) if str(x).find("(") != -1 else x)

        cluster['heavy'] = [cluster_path.stem]*len(cluster)
        cluster['patient_count'] = [cluster_path.parent.name]*len(cluster)

        df_cluster = pd.concat([df_cluster, cluster], axis=0)
    df_cluster['cancer'] = [cancer]*len(df_cluster)
    df_combined = pd.concat([df_combined, df_cluster], axis=0)

df_combined.to_csv(
    "/rsrch4/home/mol_cgenesis/EMC_BIC_rsrch4/nkdang/Sarcoma_Project/viz/mutations/data.csv", index=False)
# cluster['Timepoint'] = cluster['Timepoint'].astype("category")
# cluster['Timepoint'] = cluster['Timepoint'].cat.set_categories(categories)
# cluster.to_csv(viz_dir.joinpath(
#     cluster_path.stem+"_mean.csv"), index=False)

# patient_colors = pd.DataFrame(
#     cluster['patient_id'].unique(), columns=['patient_id'])
# colors = random.sample(['#e6194B', '#3cb44b', '#ffe119', '#4363d8', '#f58231', '#911eb4', '#42d4f4', '#f032e6', '#bfef45', '#469990',
#                        '#9A6324', '#800000', '#808000', '#000075', '#a9a9a9', '#000000', '#fabed4'], patient_colors['patient_id'].nunique())
# patient_colors['color'] = colors
# patient_colors = dict(
#     zip(patient_colors['patient_id'], patient_colors['color']))

# fig = go.Figure()

# for patient_id, g in cluster.groupby(['patient_id']):
#     fig.add_trace(go.Scatter(y=g['mutations'], mode='markers+lines',
#                              name=patient_id, showlegend=True,
#                              meta=[f"{patient_id}<br>Count {i}" for i in g['mutations']], hovertemplate='%{meta}<extra></extra>',
#                              x=g['Timepoint'],
#                              line=dict(color=patient_colors[patient_id])))
# fig.update_layout(height=800, width=1000, title_text=cluster_path.stem)
# fig.update_xaxes(categoryorder='array', categoryarray=cat)
# # fig.show()
# fig.write_html(viz_dir.joinpath(cluster_path.stem+".html"))
# break
