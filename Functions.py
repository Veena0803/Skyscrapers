# Return subset of dataframe based on columns
def populateDataframe(sky_df, columns):
    df = sky_df.set_index('RANK')
    df = df[columns] # Fetch only these columns
    return df

# Creates a slider in the sidebar
def createSlider(st, decade):
    header(st.sidebar, "By Decade")
    decade_chosen = st.sidebar.select_slider("",options=decade)
    return decade_chosen

# Build dataframe based on decade chosen
def updateDataFrame(st, df, decade_chosen):
    st.dataframe(getDataframeSubset(df, decade_chosen))

# Return subset of dataframe based on decade chosen
def getDataframeSubset(df, decade_chosen):
    result_df = df.loc[(df['COMPLETION'] < int(decade_chosen)) & (df['COMPLETION'] >= int(decade_chosen) - 10)]
    # Multi sorting by city and meters columns
    result_df.sort_values(by=['CITY', 'Meters'], ascending=[True, False], na_position='first')
    return result_df

# Get dataframe for map
def getMapDataframeSubset(df, decade_chosen):
    return df.loc[(df['COMPLETION'] < int(decade_chosen)) & (df['COMPLETION'] >= 1930)]

# Function to get the cumulative data until the decade chosen
def getAllSkyscrapersUntilDecadeChosen(df, decade_chosen):
    return df.loc[(df['COMPLETION'] <= int(decade_chosen))]

# Separator
def addMarkdownSeparator(st):
    st.markdown("""---""")

# Prints header
def header(st, url = "Progression of construction of skyscrapers across the world"):
    st.markdown(f'<p style="color:#EABC11;font-size:20px;font-weight:bold;font-family:Calibri;">{url}</p>',
                unsafe_allow_html=True)

# Print content
def content(url, st):
    st.markdown(f'<p style="color:#fff;font-size:18px;font-family:Calibri;font-weight:bold">{url}</p>',
                unsafe_allow_html=True)