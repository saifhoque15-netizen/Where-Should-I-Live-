# Where Should I Live

Where Should I Live is the final term project of the course **Programming for Data Science**.

## Usage


## Contributing

This is the group 22 project.

## Environment Data
o compile the environmental data for the cities in your dataset, I used the following resources and methodologies:

1. Pollution Index & Air Quality Index

    Source: Numbeo Pollution Index 2024 and European Environment Agency (EEA) air quality reports.

    Methodology:

        Major Cities: Specific real-time and survey-based indices were retrieved from Numbeo.

        Smaller Cities: Values were approximated using regional or country-level averages, adjusted for known industrial activity or proximity to major urban centers (e.g., cities in Northern Italy generally have higher pollution indices due to the geography of the Po Valley).

        Note: The "Air Quality Index" was calculated as the inverse of the Pollution Index for consistency (where 100 = Cleanest, 0 = Most Polluted).

2. CO2 Emissions (per capita)

    Source: Worldometer CO2 Emissions Data and Eurostat (2022/2023 estimates).

    Methodology:

        Since city-specific carbon footprint data is often unavailable or inconsistent across borders, I used the most recent country-level per capita emissions figures. This serves as a standardized baseline for comparing cities in different nations.

3. Green Space Index

    Source: HUGSI (Husqvarna Urban Green Space Index) 2024 and EEA Urban Atlas.

    Methodology:

        Mapped Cities: For cities covered by the HUGSI index or Urban Atlas, I used the specific percentage of urban area covered by vegetation.

        Estimates: For unmapped cities, I applied regional averages based on climate and urban planning characteristics (e.g., Nordic cities were assigned higher baseline percentages ~45-50%, while dense historical centers in Southern Europe were estimated between ~15-25%).
        
## License

[MIT](https://choosealicense.com/licenses/mit/)