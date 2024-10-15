

// alert("If you're seeing this, the javascript file was included successfully.");

// Shiny.addCustomMessageHandler('open_tab', function(url) {
//     console.log("Custom message handler called with URL: " + url);
//     if (url) {
//         window.open(url, '_blank');
//     } else {
//         console.log("No valid URL provided.");
//     }
// });

// To go to the page for the entire peach agreement
Shiny.addCustomMessageHandler('test_message', function(url) {
    if (url){
        window.open(url, '_blank');
    }
});


////////// TOOLTIP ////////// 
// Throttle the function handling the mousemove event to reduce 
// how often the tooltip updates: 
// It calls the function every some time.

function throttle(func, limit) {
    let inThrottle;
    return function() {
        const args = arguments;
        const context = this;
        if (!inThrottle) {
            func.apply(context, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    }
}

// This function updates the tooltip only after sometime the mouse has
// not moved.

function debounce(func, delay) {
    let timeout;
    return function() {
        const args = arguments;
        const context = this;
        clearTimeout(timeout);
        timeout = setTimeout(() => func.apply(context, args), delay);
    };
}

/// Makes tooltips based on the movements of the mouse
document.addEventListener('mousemove', throttle(function(event) {
    
    let tooltip = document.querySelector('.custom-tooltip');
    if (tooltip) {
        // console.log("javascript file loaded");
        tooltip.style.left = event.pageX - 100 + 'px';  
        tooltip.style.top = event.pageY - 100 + 'px'; 

        // system.out.printf(tooltip.textContent)

        // if (tooltip.textContent && tooltip.textContent.trim() !== "Hover over a country") {
        if (tooltip.textContent && tooltip.textContent.trim() !== "") {

            // console.log("Tooltip content:", tooltip.textContent.trim() !== "Hover over a country");
            // console.log("Tooltip content:", tooltip.textContent);
            tooltip.style.display = 'block';  // Show tooltip if hovering over a country
        } else {
            // console.log("Tooltip content:", tooltip.textContent);
            tooltip.style.display = 'none';  // Hide tooltip if not hovering over a country
        }
    }
}, 0));


// Removing the progressbar on top of the browser when the mouse moves
// NProgress.remove();