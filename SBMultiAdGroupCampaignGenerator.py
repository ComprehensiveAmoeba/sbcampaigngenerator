import streamlit as st
import pandas as pd
import random
import string
from io import BytesIO
from datetime import datetime

def generate_campaign_name(row):
    if row['Ad Format'] in ["Brand Video Ad", "Video Ad"]:
        campaign_name = "SBV_"
    elif row['Ad Format'] == "Product Collection Ad":
        campaign_name = "SB_"
    else:
        campaign_name = ""

    campaign_name += row['Brand'] + "_"

    if pd.notna(row['Product type']):
        campaign_name += row['Product type'] + "_"

    campaign_name += row['Creative ASINs'].replace(", ", "_") + "_"

    if row['Landing Page Type'] == "Store":
        campaign_name += "ST_"
    else:
        campaign_name += "DP_"

    campaign_name += row['Campaign type']

    return campaign_name

def random_string(length=10):
    letters = string.ascii_letters + string.digits
    return ''.join(random.choice(letters) for i in range(length))

def main():
    st.title("SB Multi AdGroup Campaigns Generator")

    uploaded_file = st.file_uploader("Upload Template xlsx", type="xlsx")

    if uploaded_file:
        df_template = pd.read_excel(uploaded_file, sheet_name='Template')
        df_brand_assets = pd.read_excel(uploaded_file, sheet_name='BRAND ASSETS')
        df_negative_presets = pd.read_excel(uploaded_file, sheet_name='Negative Presets')

        apply_negative_presets = st.checkbox("Apply Negative Presets")

        df_template['Mother Campaign Name'] = df_template.apply(generate_campaign_name, axis=1)

        child_campaigns = ["TOFU", "MOFU", "LOFU"]

        campaign_data = []

        for idx, row in df_template.iterrows():
            st.subheader(f"Mother Campaign: {row['Mother Campaign Name']}")
            selected_child_campaigns = []
            child_targets = {}
            for child in child_campaigns:
                if st.checkbox(f"Create {child} campaign", key=f"{row['Mother Campaign Name']}_{child}"):
                    selected_child_campaigns.append(child)
                    targets = st.text_area(f"Enter targets for {row['Mother Campaign Name']}_{child}", key=f"targets_{row['Mother Campaign Name']}_{child}")
                    child_targets[child] = targets.split("\n")

            campaign_data.append({
                "mother_campaign": row['Mother Campaign Name'],
                "selected_child_campaigns": selected_child_campaigns,
                "child_targets": child_targets,
                "row_data": row
            })

        if st.button("Generate Output File"):
            output_data = []

            today = datetime.today().strftime('%Y%m%d')

            for data in campaign_data:
                mother_campaign = data['mother_campaign']
                row = data['row_data']  # Retrieve the row data for the specific mother campaign
                for child in data['selected_child_campaigns']:
                    child_campaign_name = f"{mother_campaign}_{child}"
                    campaign_id = random_string()
                    
                    # Campaign entity
                    output_data.append({
                        'Product': "Sponsored Brands", 
                        'Entity': "Campaign", 
                        'Operation': "create", 
                        'Campaign ID': campaign_id, 
                        'Campaign Name': child_campaign_name, 
                        'Start Date': today, 
                        'State': "enabled", 
                        'Brand Entity ID': row['Brand Entity ID'], 
                        'Budget Type': "Daily", 
                        'Budget': row['Budget'], 
                        'Bid Optimization': "false"
                    })
                    
                    # Bidding adjustment by placement entities
                    for placement in ["Home", "Detail Page", "Other"]:
                        output_data.append({
                            'Product': "Sponsored Brands", 
                            'Entity': "Bidding adjustment by placement", 
                            'Operation': "create", 
                            'Campaign ID': campaign_id, 
                            'Placement': placement, 
                            'Percentage': "-30"
                        })
                    
                    # Ad Group entities
                    ad_group_ids = {name: random_string() for name in ["OW", "PH", "Branded"]}
                    for name, ad_group_id in ad_group_ids.items():
                        output_data.append({
                            'Product': "Sponsored Brands", 
                            'Entity': "Ad Group", 
                            'Operation': "create", 
                            'Campaign ID': campaign_id, 
                            'Ad Group ID': ad_group_id, 
                            'Ad Group Name': name, 
                            'Start Date': today, 
                            'State': "enabled"
                        })

                        # Ad entities
                        ad_id = random_string()
                        ad_format = row['Ad Format']
                        landing_page_url = df_brand_assets.loc[df_brand_assets['Brand'] == row['Brand'], 'Landing Page URL'].values[0]
                        brand_logo_asset_id = df_brand_assets.loc[df_brand_assets['Brand'] == row['Brand'], 'Brand Logo Asset ID'].values[0]
                        creative_headline = df_brand_assets.loc[df_brand_assets['Brand'] == row['Brand'], 'Creative Headline'].values[0]
                        
                        ad_data = {
                            'Product': "Sponsored Brands", 
                            'Entity': ad_format, 
                            'Operation': "create", 
                            'Campaign ID': campaign_id, 
                            'Ad Group ID': ad_group_id, 
                            'Ad ID': ad_id, 
                            'Ad Name': "Evergreen", 
                            'Start Date': today, 
                            'State': "enabled", 
                            'Landing Page URL': landing_page_url, 
                            'Landing Page Type': row['Landing Page Type'], 
                            'Creative ASINs': row['Creative ASINs'], 
                            'Brand name': row['Brand'], 
                            'Brand Logo Asset ID': brand_logo_asset_id, 
                            'Creative Headline': creative_headline
                        }
                        
                        if ad_format != "Product Collection Ad":
                            ad_data['Video Asset IDs'] = df_brand_assets.loc[df_brand_assets['Brand'] == row['Brand'], 'Video Asset IDs'].values[0]
                        else:
                            ad_data['Custom Images'] = df_brand_assets.loc[df_brand_assets['Brand'] == row['Brand'], 'Custom Images'].values[0]
                        
                        output_data.append(ad_data)
                    
                    # Keyword entities for OW and PH
                    for ad_group_name in ["OW", "PH"]:
                        for target in data['child_targets'][child]:
                            output_data.append({
                                'Product': "Sponsored Brands", 
                                'Entity': "Keyword", 
                                'Operation': "create", 
                                'Campaign ID': campaign_id, 
                                'Ad Group ID': ad_group_ids[ad_group_name], 
                                'Keyword ID': random_string(), 
                                'Start Date': today, 
                                'State': "enabled", 
                                'Bid': row['Bid'], 
                                'Keyword Text': target, 
                                'Match Type': "Exact" if ad_group_name == "OW" else "Phrase"
                            })
                    
                    # Keyword entities for Branded
                    for match_type in ["Phrase", "Exact"]:
                        output_data.append({
                            'Product': "Sponsored Brands", 
                            'Entity': "Keyword", 
                            'Operation': "create", 
                            'Campaign ID': campaign_id, 
                            'Ad Group ID': ad_group_ids["Branded"], 
                            'Keyword ID': random_string(), 
                            'Start Date': today, 
                            'State': "enabled", 
                            'Bid': row['Bid'], 
                            'Keyword Text': row['Brand'], 
                            'Match Type': match_type
                        })
                    
                    # Negative Keyword entities for PH
                    for target in data['child_targets'][child]:
                        output_data.append({
                            'Product': "Sponsored Brands", 
                            'Entity': "Negative Keyword", 
                            'Operation': "create", 
                            'Campaign ID': campaign_id, 
                            'Ad Group ID': ad_group_ids["PH"], 
                            'Keyword ID': random_string(), 
                            'Start Date': today, 
                            'State': "enabled", 
                            'Keyword Text': target, 
                            'Match Type': "Negative Exact"
                        })

            df_output = pd.DataFrame(output_data, columns=[
                'Product', 'Entity', 'Operation', 'Campaign ID', 'Portfolio ID', 'Ad Group ID', 'Ad ID', 'Keyword ID', 'Product Targeting ID',
                'Campaign Name', 'Ad Group Name', 'Ad Name', 'Start Date', 'End Date', 'State', 'Brand Entity ID', 'Budget Type', 
                'Budget', 'Bid Optimization', 'Product Location', 'Bid', 'Placement', 'Percentage', 'Keyword Text', 'Match Type', 
                'Product Targeting Expression', 'Landing Page URL', 'Landing Page ASINs', 'Landing Page Type', 'Brand name', 
                'Brand Logo Asset ID', 'Brand Logo Crop', 'Custom Images', 'Creative Headline', 'Creative ASINs', 
                'Video Asset IDs', 'Subpages'
            ])
            output = BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                df_output.to_excel(writer, index=False, sheet_name='Campaigns')

            st.download_button(
                label="Download Output File",
                data=output,
                file_name="campaigns_output.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

if __name__ == "__main__":
    main()
