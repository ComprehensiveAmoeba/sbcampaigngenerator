# SB Multi AdGroup Campaigns Generator

## Overview
The SB Multi AdGroup Campaigns Generator is a Streamlit app designed to automate the creation of Amazon Sponsored Brand campaigns with multiple ad groups. This tool facilitates the generation of structured campaign files based on user inputs, ensuring efficient and streamlined campaign setup.

## Features
- **Template Upload**: Upload a predefined Excel template containing campaign data.
- **Campaign Name Generation**: Automatically generates campaign names based on specific criteria.
- **Ad Group Creation**: Enables the creation of multiple ad groups within each campaign.
- **Keyword and Negative Keyword Management**: Allows for the input and assignment of keywords and negative keywords.
- **Output File Generation**: Generates an Excel file containing the structured campaign data ready for upload to Amazon.

## How to Use
1. **Prepare Your Data**: Use the provided g-sheet template (get it from ComprehensiveAmoeba) to format your campaign data. Ensure all required fields are filled out correctly.
2. **Launch the App**: Start the [Streamlit app](https://campaigncreationapp.streamlit.app/). You'll see an interface with an option to upload your Excel file.
3. **Upload Template File**: Click on 'Choose a file' and select your prepared Excel template.
4. **Select Options**: Choose whether to apply negative presets and select which child campaigns to create.
5. **Enter Targets**: For each child campaign, input the desired targets.
6. **Generate Output File**: Once all data is entered, click 'Generate Output File'. The app will process the data and provide a button to download the generated Excel campaign file.

## Mandatory Input Fields
The following fields are mandatory for the campaign creation process:
1. **Brand**: The brand associated with the campaign.
2. **Ad Format**: The format of the ad, such as "Brand Video Ad" or "Product Collection Ad".
3. **Creative ASINs**: ASINs of the products featured in the ad.
4. **Landing Page Type**: The type of landing page, either "Store" or "Detail Page".
5. **Campaign type**: The type of campaign, such as "Awareness" or "Consideration".
6. **Budget**: The daily budget for the campaign.
7. **Bid**: The bid amount for keywords.

## Optional Fields
- **Product type**
- **Brand Entity ID**

## Ad Group Options
- **TOFU**: Top of Funnel campaign.
- **MOFU**: Middle of Funnel campaign.
- **BOFU**: Bottom of Funnel campaign.
- **Other**: opt out of the funnelling naming conventions or create a tag at the end of the campaign name.

## Dependencies
- Streamlit
- Pandas
- Openpyxl
- Python's Random and String libraries
- Python's datetime module

## App Code Structure
- `generate_campaign_name`: Generates a campaign name based on input data.
- `random_string`: Generates a random string for unique IDs.
- `main`: The main function that defines the Streamlit app layout and logic.

- ## Limitations
While the SB Multi AdGroup Campaigns Generator offers a range of features, some functionalities are still under development and are not currently available. These planned features include:

- **Negative Presets**: Although there is an option to apply negative presets, this feature is not yet functional.
- **CAT and PAT Mother Campaign Targets**: The ability to create CAT (Category) and PAT (Product Attribute Targeting) mother campaign targets is planned but not yet implemented.
- **Keyword Universe Segmentation**: Segmenting the keyword universe directly within the app is not currently supported.
- **Old Format Campaign Migration**: Migrating old format campaigns directly within the app is a planned feature but is not yet available.

Please keep these limitations in mind while using the app. Future updates will include these features to enhance functionality and usability.


## Troubleshooting
- **Invalid Data Format**: Ensure your Excel file matches the format in the provided template.
- **Error During File Generation**: Check if all fields in the template are correctly filled. Ensure there are no missing mandatory fields.

## Support
For additional help or to report issues, please contact ComprehensiveAmoeba ;).
