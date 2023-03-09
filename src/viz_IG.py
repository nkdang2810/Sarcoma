import pandas as pd


data_combined = pd.DataFrame(columns=[
                             'IG_subtypes', 'patient_id', 'Timepoint', 'consensus_count', 'total', 'normalized_count'])

for cancer in ["PBMC_DDLPS", "PBMC_UPS", "tumor_DDLPS", "tumor_UPS"]:
    df = pd.read_csv(
        f"/rsrch4/home/mol_cgenesis/EMC_BIC_rsrch4/nkdang/Sarcoma_Project/results/{cancer}/heavy/data_clean.csv").astype({"patient_id": str})
    meta = pd.read_csv(
        f"/rsrch4/home/mol_cgenesis/EMC_BIC_rsrch4/nkdang/Sarcoma_Project/meta/{cancer}.csv").astype({"patient_id": str})
    df['IG_subtypes'] = df['c_call'].str[:4]
    df['IG_subtypes'] = df['IG_subtypes'].fillna("Unclassified")
    df = df[['IG_subtypes', 'patient_id', 'sample_id', 'consensus_count']]
    data = df[['IG_subtypes', 'patient_id', 'sample_id', 'consensus_count']
              ].value_counts(dropna=False).rename("count").reset_index()
    data.to_csv(
        f"/rsrch4/home/mol_cgenesis/EMC_BIC_rsrch4/nkdang/Sarcoma_Project/viz/IG_subtypes/{cancer}_data_0.csv", index=False)

    data = data.merge(meta[["sample_id", "Timepoint"]],
                      how="left", left_on="sample_id", right_on="sample_id")
    data.to_csv(
        f"/rsrch4/home/mol_cgenesis/EMC_BIC_rsrch4/nkdang/Sarcoma_Project/viz/IG_subtypes/{cancer}_data_1.csv", index=False)

    data_grouped = data.groupby(['IG_subtypes', 'patient_id', 'sample_id', 'Timepoint'])[
        'consensus_count'].sum().reset_index()
    data_grouped.to_csv(
        f"/rsrch4/home/mol_cgenesis/EMC_BIC_rsrch4/nkdang/Sarcoma_Project/viz/IG_subtypes/{cancer}_data_2.csv", index=False)

    data_mean = data_grouped.groupby(['IG_subtypes', 'patient_id', 'Timepoint'])[
        'consensus_count'].mean().reset_index()
    data_mean.to_csv(
        f"/rsrch4/home/mol_cgenesis/EMC_BIC_rsrch4/nkdang/Sarcoma_Project/viz/IG_subtypes/{cancer}_data_3.csv", index=False)

    count_patient_time = pd.DataFrame(data_mean.groupby(
        ['patient_id', "Timepoint"])['consensus_count'].sum())
    data_mean['total'] = data_mean.apply(lambda x: count_patient_time.loc[(
        x['patient_id'], x['Timepoint'])]['consensus_count'], axis=1)
    data_mean['normalized_count'] = data_mean.apply(
        lambda x: x['consensus_count']/x['total'], axis=1)
    data_mean['cancer'] = [cancer]*len(data_mean)
    data_mean.to_csv(
        f"/rsrch4/home/mol_cgenesis/EMC_BIC_rsrch4/nkdang/Sarcoma_Project/viz/IG_subtypes/{cancer}_data_4.csv", index=False)

    data_combined = pd.concat([data_combined, data_mean], axis=0)

data_combined.to_csv(
    "/rsrch4/home/mol_cgenesis/EMC_BIC_rsrch4/nkdang/Sarcoma_Project/viz/IG_subtypes/data.csv", index=False)
