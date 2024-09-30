from shiny import ui
from pathlib import Path

css_file = Path(__file__).parent / "css" / "styles.css"
js_file = Path(__file__).parent / "www" / "download_page.js"

app_ui = ui.page_fluid(
    # ui.head_content(ui.include_css("styles.css")), 
    ui.include_css(css_file),
    # ui.head_content(ui.include_js("www/download_page.js")),
    ui.include_js(js_file),
    ui.div(
        ui.navset_pill(  
            ui.nav_panel("Data", 
                ui.output_ui("map_ui"),     
                ui.output_ui("country_details_ui"), 
                ui.output_ui("agreement_details_ui")    
            ),          
                ui.nav_panel("About",
                            ui.h2("About This Application"),
                            ui.p("This application is designed to..."),
                            ),
            id="tab",
        ),
        class_="custom-nav-tabs" 
    )  
)