import urllib.request
import geopandas as gpd
import requests

#List of building datasets from different French regions that are availabe for download. Not the best implementation if you'd like to generalize a script
#that could download data from any region specified. 
region_data_list = [{"name": "bnb_export_93", "url": "https://static.data.gouv.fr/resources/base-de-donnee-nationale-des-batiments-version-0-6/20220427-184603/bnb-export-93.gpkg.zip"}, {"name": "bnb_export_75", "url": "https://static.data.gouv.fr/resources/base-de-donnee-nationale-des-batiments-version-0-6/20220427-184828/bnb-export-75.gpkg.zip"}]

#downloads a zip file from url 
def download_zip_file(title,url):
    zip_file = requests.get(url)
    open("{}.zip".format(title), "wb").write(zip_file.content)
    
#Downloads all the zip files defined in region_data_list
def download_bnb_zip_files():
    for region_data in region_data_list:
        download_zip_file(region_data["name"],region_data["url"])

def data_mapping(df1,df2):
    return df1.append(df2)
    
#Writes the data into a csv-file
def write_to_csv(df,title):
    df.to_csv(path_or_buf=title,index=None)


#Explainations for the designated tasks
def main():
    #1st step:
    download_bnb_zip_files()
    #I couldn't find a good way to unzip a file using python during the time I had, nor could i get geopandas to read the gkpg-file directly from the zip.
    #I therefore had to manually unzip the folders at this point. 

    #2nd step:
    #Loads the region data into dataframes, which are placed in an array
    bnb_df_list = []
    for region_data in region_data_list:
        bnb_local_directory = "{0}/{0}.gpkg".format(region_data["name"])
        print(bnb_local_directory)
        bnb_df = gpd.read_file(bnb_local_directory)
        bnb_df_list.append(bnb_df)

    #Writes the data for region 93 into a csv-file
    write_to_csv(bnb_df_list[0],region_data_list[0]["name"])

    #3rd step:
    #The two data sets are already extracts from a larger dataset, and therefore the mapping can be easily done by simply appending the two datasets together
    mappeddf = bnb_df_list[0].append(bnb_df_list[1])

    #I have chosen array as data structure and csv-format for my data. 
    #I believe a linear array structure would suffice here, and it is also the most straightforward solution. The data is not even that big, so efficiency is not the biggest issue here. 
    #csv is a common way to store data and seems to work well as long as you stick to two-dimensional data structure.
    write_to_csv(mappeddf,"mappeddata")

    #I think if I were to prepare the data further, I would remove many of the features from the data.
    #A lot of the features, such as zipcode and geospatial data, are unecessary if what you want is to predict the energy efficiency of a building. 
    
    #Step 4:
    #You wouldn't be able to read this if I hadn't done this step :^)
