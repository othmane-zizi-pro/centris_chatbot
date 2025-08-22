import streamlit as st
import numpy as np
from numpy.linalg import norm
import plotly.graph_objects as go
from buildings_data import buildings  # Import the buildings dictionary

# Define option dictionaries
universities_dict = {
    "1": "McGill University",
    "2": "Concordia University",
    "3": "Université de Montréal",
    "4": "HEC Montréal",
    "5": "Polytechnique Montréal"
}
accommodation_dict = {
    "1": "No Preference",
    "2": "Condo/Apartment",
    "3": "Townhouse"
}
bedrooms_townhouse_dict = {
    "1": "2 Bedrooms",
    "2": "3 Bedrooms",
    "3": "4+ Bedrooms"
}
bedrooms_condo_dict = {
    "1": "Studio",
    "2": "1 Bedroom",
    "3": "2 Bedrooms"
}
bedrooms_nopref_dict = {
    "1": "Studio",
    "2": "1 Bedroom",
    "3": "2 Bedrooms",
    "4": "3 Bedrooms",
    "5": "4+ Bedrooms"
}
amenities_dict = {
    "1": "Gym",
    "2": "Indoor Pool",
    "3": "Outdoor Pool",
    "4": "Garden",
    "5": "Patio",
    "6": "Library",
    "7": "Social Room",
    "8": "Sauna",
    "9": "Jacuzzi",
    "10": "BBQ",
    "11": "Laundry Room"
}
appliances_dict = {
    "1": "Dishwasher",
    "2": "In-unit Washing Machine",
    "3": "In-unit Dryer",
    "4": "A/C",
    "5": "Heater",
    "6": "Microwave"
}
yes_no_dict = {
    "1": "No preference",
    "2": "Yes"
}

# Streamlit app layout
st.title("Building Recommendation System")

name = st.text_input("Please enter your name:")

st.header("University")
university_key = st.selectbox("What university will you be attending?", list(universities_dict.keys()), format_func=lambda k: universities_dict[k])
university = universities_dict[university_key]

st.header("Distance Preferences")
campus_dist_key = st.radio("Do you want to be within 1 km from campus?", list(yes_no_dict.keys()), format_func=lambda k: yes_no_dict[k].capitalize())
campus_dist = yes_no_dict[campus_dist_key]

metro_dist_key = st.radio("Do you want to be within 500 m from a metro station?", list(yes_no_dict.keys()), format_func=lambda k: yes_no_dict[k].capitalize())
metro_dist = yes_no_dict[metro_dist_key]

st.header("Accommodation Type")
acc_key = st.selectbox("What type of accommodation are you looking for?", list(accommodation_dict.keys()), format_func=lambda k: accommodation_dict[k])
accommodation = accommodation_dict[acc_key]

st.header("Number of Bedrooms")
if accommodation == "Townhouse":
    bedrooms_key = st.selectbox("How many bedrooms do you want?", list(bedrooms_townhouse_dict.keys()), format_func=lambda k: bedrooms_townhouse_dict[k])
    bedrooms = bedrooms_townhouse_dict[bedrooms_key]
elif accommodation == "Condo/Apartment":
    bedrooms_key = st.selectbox("How many bedrooms do you want?", list(bedrooms_condo_dict.keys()), format_func=lambda k: bedrooms_condo_dict[k])
    bedrooms = bedrooms_condo_dict[bedrooms_key]
else:
    bedrooms_key = st.selectbox("How many bedrooms do you want?", list(bedrooms_nopref_dict.keys()), format_func=lambda k: bedrooms_nopref_dict[k])
    bedrooms = bedrooms_nopref_dict[bedrooms_key]

st.header("Building Height")
if accommodation != "Townhouse":
    ten_floors_key = st.radio("Do you want your building to be taller than 10 floors?", list(yes_no_dict.keys()), format_func=lambda k: yes_no_dict[k].capitalize())
    ten_floors = yes_no_dict[ten_floors_key]
else:
    ten_floors = 'Not Applicable'

st.header("Price Range")
min_price = st.number_input("What is your minimum price per month?", min_value=0, value=0)
max_price = st.number_input("What is your maximum price per month?", min_value=0, value=10000)
if max_price < min_price:
    st.error("Maximum price cannot be less than minimum price.")

# Define callbacks to clear selections
def clear_amenities():
    if st.session_state.no_amen_pref:
        st.session_state.amenities_multi = []

def clear_appliances():
    if st.session_state.no_app_pref:
        st.session_state.appliances_multi = []

st.header("Amenities (up to 3)")
st.checkbox("No Preference for Amenities", key="no_amen_pref", on_change=clear_amenities)
if st.session_state.no_amen_pref:
    amenities_selected = 'No preference'
else:
    amenities_options = [amenities_dict[k] for k in amenities_dict]
    amenities_selected = st.multiselect("Select up to 3 amenities:", amenities_options, max_selections=3, key="amenities_multi")

st.header("Appliances (up to 3)")
st.checkbox("No Preference for Appliances", key="no_app_pref", on_change=clear_appliances)
if st.session_state.no_app_pref:
    appliances_selected = 'No preference'
else:
    appliances_options = [appliances_dict[k] for k in appliances_dict]
    appliances_selected = st.multiselect("Select up to 3 appliances:", appliances_options, max_selections=3, key="appliances_multi")

# Collect preferences
preferences = {
    "name": name,
    "university": university,
    "within_1km_campus": campus_dist,
    "within_500m_metro": metro_dist,
    "accommodation": accommodation,
    "bedrooms": bedrooms,
    "over_ten_floors": ten_floors,
    "min_price": min_price,
    "max_price": max_price,
    "amenities": amenities_selected,
    "appliances": appliances_selected
}

if st.button("Get Recommendations"):
    # Display user preferences nicely
    st.header("Your Preferences")
    st.write(f"**Name:** {preferences['name']}")
    st.write(f"**University:** {preferences['university']}")
    st.write(f"**Within 1km of Campus:** {preferences['within_1km_campus']}")
    st.write(f"**Within 500m of Metro:** {preferences['within_500m_metro']}")
    st.write(f"**Accommodation Type:** {preferences['accommodation']}")
    st.write(f"**Number of Bedrooms:** {preferences['bedrooms']}")
    st.write(f"**Over 10 Floors:** {preferences['over_ten_floors']}")
    st.write(f"**Price Range:** ${preferences['min_price']} - ${preferences['max_price']}")
    amenities_str = ', '.join(preferences['amenities']) if isinstance(preferences['amenities'], list) else preferences['amenities']
    st.write(f"**Amenities:** {amenities_str}")
    appliances_str = ', '.join(preferences['appliances']) if isinstance(preferences['appliances'], list) else preferences['appliances']
    st.write(f"**Appliances:** {appliances_str}")

    # Recommend function (adapted from your code)
    def recommend(preferences, buildings):
        university = preferences['university']
        within_campus = preferences['within_1km_campus']
        within_metro = preferences['within_500m_metro']
        acc = preferences['accommodation']
        bedrooms = preferences['bedrooms']
        over_ten = preferences['over_ten_floors']
        min_p = preferences['min_price']
        max_p = preferences['max_price']
        amens = preferences['amenities']
        if amens == 'No preference':
            amens = []
        apps = preferences['appliances']
        if apps == 'No preference':
            apps = []
        # Define all possible categories for vectorization
        all_accom = ["Condo/Apartment", "Townhouse"]
        all_beds = ["Studio", "1 Bedroom", "2 Bedrooms", "3 Bedrooms", "4+ Bedrooms"]
        all_amen = ["Gym", "Indoor Pool", "Outdoor Pool", "Garden", "Patio", "Library", "Social Room", "Sauna", "Jacuzzi", "BBQ", "Laundry Room"]
        all_app = ["Dishwasher", "In-unit Washing Machine", "In-unit Dryer", "A/C", "Heater", "Microwave"]
        # User vector components
        # Accommodation
        user_accom = [1 if acc == a else 0 for a in all_accom]
        if acc == "No Preference":
            user_accom = [0] * len(all_accom)
        
        # Over ten floors
        user_floors = 1 if over_ten == 'Yes' else 0
        
        # Bedrooms (user selects one specific)
        user_beds = [1 if bedrooms == b else 0 for b in all_beds]
        
        # Amenities
        user_amen = [1 if a in amens else 0 for a in all_amen]
        
        # Appliances
        user_app = [1 if a in apps else 0 for a in all_app]
        
        # Close to campus
        user_close_campus = 1 if within_campus == 'Yes' else 0
        
        # Close to metro
        user_close_metro = 1 if within_metro == 'Yes' else 0
        
        # Affordability (always care)
        user_afford = 1
        # Full user vector
        user_vec = np.array(user_accom + [user_floors] + user_beds + user_amen + user_app + [user_close_campus, user_close_metro, user_afford])
        user_norm = norm(user_vec)
        if user_norm == 0:
            st.error("Unable to compute similarities due to empty preference vector.")
            return
        # Compute similarities for ALL buildings
        sims = []
        for name, data in buildings.items():
            # Building vector components, neutralized if no user preference
            b_accom = [1 if data.get('accommodation') == a else 0 for a in all_accom] if acc != "No Preference" else [0] * len(all_accom)
            b_floors = 1 if data.get('over_ten_floors') == 'yes' else 0 if over_ten == 'Yes' else 0
            b_beds = [1 if b in data.get('unit_types', []) else 0 for b in all_beds]
            b_amen = [1 if a in data.get('amenities', []) else 0 for a in all_amen] if amens else [0] * len(all_amen)
            b_app = [1 if a in data.get('appliances', []) else 0 for a in all_app] if apps else [0] * len(all_app)
            dist = data.get('distance_to_campuses_km', {}).get(university, float('inf'))
            b_close_campus = 1 / (1 + dist) if dist != float('inf') and within_campus == 'Yes' else 0
            b_close_metro = 1 if data.get('within_500m_metro') == 'yes' and within_metro == 'Yes' else 0
            if bedrooms in data.get('prices_monthly', {}):
                price = data['prices_monthly'][bedrooms]
            else:
                price = float('inf')
            if price == float('inf'):
                b_afford = 0
            else:
                center = (min_p + max_p) / 2
                width = (max_p - min_p) / 2 + 1e-6
                b_afford = np.exp( - ((price - center) / width) ** 2 )
            b_vec = np.array(b_accom + [b_floors] + b_beds + b_amen + b_app + [b_close_campus, b_close_metro, b_afford])
            b_norm = norm(b_vec)
            if b_norm == 0:
                sim = 0.0
            else:
                sim = np.dot(user_vec, b_vec) / (user_norm * b_norm)
            sims.append((sim, name))
        
        # Sort and display top 10
        sims.sort(reverse=True, key=lambda x: x[0])
    
        st.header("Recommended buildings (sorted by cosine similarity):")
    
        # Display top building before graph
        st.subheader("Top Building Recommendation")
        top_sim, top_name = sims[0]
        st.markdown(f"**1. {top_name}**: *similarity score {top_sim:.4f}*")
        top_data = buildings.get(top_name, {})
        st.write(f"**Accommodation:** {top_data.get('accommodation', 'Unknown')}")
        st.write(f"**Unit Types:** {', '.join(top_data.get('unit_types', [])) or 'None'}")
        st.write(f"**Amenities:** {', '.join(top_data.get('amenities', [])) or 'None'}")
        st.write(f"**Appliances:** {', '.join(top_data.get('appliances', [])) or 'None'}")
        st.write(f"**Distance to {university}:** {top_data.get('distance_to_campuses_km', {}).get(university, 'Unknown')} km")
        st.write(f"**Within 500m of Metro:** {top_data.get('within_500m_metro', 'Unknown')}")
        st.write("**Prices Monthly:**")
        prices = top_data.get('prices_monthly', {})
        if prices:
            for k, v in prices.items():
                st.write(f"- {k}: ${v}")
        else:
            st.write("None")
        st.write(f"**Over 10 Floors:** {top_data.get('over_ten_floors', 'Unknown')}")
        st.markdown("---")  # Separator before graph
    
        # Create Plotly bar graph for top 10 buildings
        names = [name for _, name in sims[:10]]
        scores = [sim for sim, _ in sims[:10]]
        colors = ['red' if i == 0 else 'blue' for i in range(len(names))]  # Red for highest, blue for others
        text = ['recommended' if i == 0 else '' for i in range(len(names))]  # Label for highest
        
        fig = go.Figure(data=[
            go.Bar(
                x=names,
                y=scores,
                marker_color=colors,
                text=text,
                textposition='auto'
            )
        ])
        fig.update_layout(
            title="Top 10 Recommended Buildings by Similarity Score",
            xaxis_title="Building Name",
            yaxis_title="Similarity Score",
            showlegend=False
        )
        st.plotly_chart(fig)
    
        # Display remaining 9 buildings after graph
        for i, (sim, name) in enumerate(sims[1:10], start=2):  # Skip the first (already shown)
            st.markdown(f"**{i}. {name}**: *similarity score {sim:.4f}*")
            data = buildings.get(name, {})
            st.write(f"**Accommodation:** {data.get('accommodation', 'Unknown')}")
            st.write(f"**Unit Types:** {', '.join(data.get('unit_types', [])) or 'None'}")
            st.write(f"**Amenities:** {', '.join(data.get('amenities', [])) or 'None'}")
            st.write(f"**Appliances:** {', '.join(data.get('appliances', [])) or 'None'}")
            st.write(f"**Distance to {university}:** {data.get('distance_to_campuses_km', {}).get(university, 'Unknown')} km")
            st.write(f"**Within 500m of Metro:** {data.get('within_500m_metro', 'Unknown')}")
            st.write("**Prices Monthly:**")
            prices = data.get('prices_monthly', {})
            if prices:
                for k, v in prices.items():
                    st.write(f"- {k}: ${v}")
            else:
                st.write("None")
            st.write(f"**Over 10 Floors:** {data.get('over_ten_floors', 'Unknown')}")
            st.markdown("---")  # Horizontal line for separation and white space

    recommend(preferences, buildings)