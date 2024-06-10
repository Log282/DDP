// Function to handle clicking on the lens image for Secondary documentation
function viewSecondary() {
    // TODO: display secondary documentation
    console.log("Secondary documentation should be viewed"); // comment out when done
  }
  
  // Function to handle clicking on the lens image for KYC documentation
  function viewKYC() {
    // TODO: display KYC
    console.log("KYC should be viewed"); // comment out when done
  }
  
  // Function to show tooltip on hover for lens images
  function showTooltip(element) {
    const dataInfo = element.dataset.info;
    const tooltip = document.createElement('div');
    tooltip.classList.add('tooltip');
    tooltip.textContent = dataInfo;
  
    const tooltipLeft = element.offsetLeft + element.clientWidth + 10;
    const tooltipTop = element.offsetTop;
  
    tooltip.style.left = `${tooltipLeft}px`;
    tooltip.style.top = `${tooltipTop}px`;
  
    document.body.appendChild(tooltip);
  
    // Store reference to tooltip in the element itself
    element.hoverTooltip = tooltip;
  }
  
  // Function to hide tooltip when mouse moves out for lens images
  function hideTooltip() {
    const tooltips = document.querySelectorAll('.tooltip');
    tooltips.forEach(tooltip => tooltip.remove());
  }
  
  // Remove tooltip when lens image is clicked
  document.addEventListener('click', function(event) {
    if (event.target.classList.contains('hover-info') && event.target.hoverTooltip) {
      event.target.hoverTooltip.remove();
    }
  });
  
  
  function testFunc(){
    console.log("it works")
  }
  
  function toggleDropdown() {
    var dropdown = document.getElementById("kycDropdown");
    dropdown.classList.toggle("show");
  }
  
  // Close the dropdown 
  window.onclick = function(event) {
    if (!event.target.matches('.highlight')) {
        var dropdowns = document.getElementsByClassName("dropdown-content");
        for (var i = 0; i < dropdowns.length; i++) {
            var openDropdown = dropdowns[i];
            if (openDropdown.classList.contains('show')) {
                openDropdown.classList.remove('show');
            }
        }
    }
  }
  
  function redirectOnChange() {
    var selectElement = document.getElementById("customerType");
    var selectedValue = selectElement.options[selectElement.selectedIndex].value;
  
    if (selectedValue === "New-Application") {
        window.location.href = "{% url 'new_application' %}";
    }
  }
  
  // hover-info.js
  
  function applyHoverInfoBehavior() {
    const hoverInfoElements = document.querySelectorAll('.hover-info');
  
    hoverInfoElements.forEach(element => {
      element.addEventListener('mouseover', function() {
        const dataInfo = this.dataset.info; 
        const tooltip = document.createElement('div');
        tooltip.classList.add('hover-info-tooltip'); 
        tooltip.textContent = dataInfo;
  
        
        const tooltipLeft = this.offsetLeft + this.clientWidth + 10; 
        const tooltipTop = this.offsetTop;
  
        tooltip.style.left = `${tooltipLeft}px`;
        tooltip.style.top = `${tooltipTop}px`;
  
        document.body.appendChild(tooltip);
      });
  
      element.addEventListener('mouseout', function() {
        const tooltips = document.querySelectorAll('.hover-info-tooltip');
        tooltips.forEach(tooltip => tooltip.remove());
      });
    });
  
    console.log('Hover info behavior applied!');
  }
  
  
  window.addEventListener('DOMContentLoaded', applyHoverInfoBehavior);
  
  //VIEW DOCUMENT (LENS)
  var modalLink = document.getElementById("modalLink");
  
  // function openModal(fileURL) {
  
  //     modalLink.href = fileURL;
  //     modalLink.target = "_blank"; // Open in a new tab or window
  
  //     modalLink.click();
  // }
  
  function openModal(fileInputId) {
    const fileInput = document.getElementById(fileInputId);
    if (fileInput.files.length > 0) {
        const file = fileInput.files[0];
        const fileURL = URL.createObjectURL(file);
  
        window.open(fileURL, '_blank');
    }
  }
  
  // Load JSON file:
  async function getHoverText(key) {
    const jsonUrl = "./hover-info.json";
  
    try {
      const response = await fetch(jsonUrl);
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      const data = await response.json();
      
      // Check if the key exists in the JSON data
      if (data.hasOwnProperty(key)) {
        return data[key];
      } else {
        console.error(`Key '${key}' not found in JSON data`);
        return key;
      }
    } catch (error) {
      console.error('Error fetching JSON:', error);
      return failGetHoverText(key); // Should return null, this just calls the json within the script itself
    }
  }
  
  // Function to handle clicking on the lens image for KYC documentation
  function viewKYC() {
    // TODO: display KYC
    console.log("KYC should be viewed"); // comment out when done
  }
  
  // Function to handle mouseover event and display tooltip
  function applyHoverInfoBehavior() {
    const hoverInfoElements = document.querySelectorAll('.hover-info');
  
    hoverInfoElements.forEach(element => {
      element.addEventListener('mouseover', async function() {
        const dataInfo = this.dataset.info;
        const tooltipText = await getHoverText(dataInfo); // Fetch hover text from JSON file
        const tooltip = document.createElement('div');
        tooltip.classList.add('hover-info-tooltip');
        tooltip.textContent = tooltipText || "Hover info not available"; // Display fetched text or fallback message
  
        const tooltipLeft = this.offsetLeft + this.clientWidth + 10; 
        const tooltipTop = this.offsetTop;
  
        tooltip.style.left = `${tooltipLeft}px`;
        tooltip.style.top = `${tooltipTop}px`;
  
        document.body.appendChild(tooltip);
      });
  
      element.addEventListener('mouseout', function() {
        const tooltips = document.querySelectorAll('.hover-info-tooltip');
        tooltips.forEach(tooltip => tooltip.remove());
      });
    });
  
    console.log('Hover info behavior applied!');
  }
  
  window.addEventListener('DOMContentLoaded', applyHoverInfoBehavior);
  
  //Adding event listener to the search input field
  
  document.getElementById("gaiaLinkButton").addEventListener("click", function() {
    var inputValue = document.getElementById("searchInput").value;
    var searchType = document.getElementById("searchType").value;
    var apiUrl;
  
    if (searchType === "account") {
        apiUrl = "http://gaiadev3.systematrix.ai/external_link/" + inputValue + "/account";
    } else if (searchType === "party") {
        apiUrl = "http://gaiadev3.systematrix.ai/external_link/" + inputValue + "/party";
    }
  
       // Open the URL in a new tab
       window.open(apiUrl, '_blank');
      });
  
  
  
      function retrieveRecentImage(documentType) {
        $.ajax({
            url: `/retrieve_recent_image/${documentType}/`,
            type: 'GET',
            success: function(data) {
                // Update the href attribute of the anchor tag
                $('#recentImageLink').attr('href', data);
            },
            error: function(xhr, status, error) {
                console.error(error);
                alert('No recent image found');
            }
        });
    }



// document.getElementById('uploadForm').addEventListener('submit', function() {
//   document.getElementById('loading-spinner').style.display = 'block';
// });


//new-ranjith
// New JavaScript function to handle form submission and display success message

// function handleFormSubmission() {
  
//   const form = document.querySelector(form[action="{% url 'save_application' %}"]);
//   form.addEventListener('submit', function(event) {
//       event.preventDefault();  // Prevent default form submission

//       const formData = new FormData(form);
//       const submitButton = form.querySelector('input[type="submit"]');
//       submitButton.disabled = true;  // Disable the submit button to prevent multiple submissions

//       fetch(form.action, {
//           method: 'POST',
//           body: formData,
//           headers: {
//               'X-CSRFToken': form.querySelector('input[name="csrfmiddlewaretoken"]').value
//           }
//       })
//       .then(response => response.json())
//       .then(data => {
//           submitButton.disabled = false;  // Re-enable the submit button
//           const messageDiv = document.getElementById('messageDiv');
//           messageDiv.textContent = `Record ${data.unique_id} created and stored`;
//           messageDiv.style.color = 'green';
//       })
//       .catch(error => {
//           submitButton.disabled = false;  // Re-enable the submit button
//           const messageDiv = document.getElementById('messageDiv');
//           messageDiv.textContent = 'An error occurred. Please try again.';
//           messageDiv.style.color = 'red';
//       });
//   });
// }

// // Call the handleFormSubmission function when the DOM content is loaded
// document.addEventListener('DOMContentLoaded', function() {
//   handleFormSubmission();
// });

// document.getElementById('uploadForm').addEventListener('submit', function() {
//   document.getElementById('loading-spinner').style.display = 'block';
// });
  


// document.getElementById("uploadForm").addEventListener("submit", function(event) {
//   event.preventDefault();
//   var formData = new FormData(this);

//   fetch('/new/', {
//       method: 'POST',
//       body: formData
//   })
//   .then(response => response.json())
//   .then(data => {
//       // Populate form fields with extracted information
//       if (data.Name) {
//           document.getElementById("fname1").value = data.Name.split(' ')[0];
//           document.getElementById("lname1").value = data.Name.split(' ')[1];
//       }
//       if (data.Address) {
//           document.getElementById("sadd").value = data.Address;
//       }
//       if (data["Date of Birth"]) {
//           document.getElementById("date1").value = data["Date of Birth"];
//       }
//       if (data["Driving Licence Number"]) {
//           document.getElementById("idno1").value = data["Driving Licence Number"];
//       }
//   })
//   .catch(error => console.error('Error:', error));
// });


    
    
    
window.addEventListener('DOMContentLoaded', applyHoverInfoBehavior);
  
// Adding event listener to the search input field
  
document.getElementById("gaiaLinkButton").addEventListener("click", function() {
    var inputValue = document.getElementById("searchInput").value;
    var searchType = document.getElementById("searchType").value;
    var apiUrl;
  
    if (searchType === "account") {
        apiUrl = "http://gaiadev3.systematrix.ai/external_link/" + inputValue + "/account";
    } else if (searchType === "party") {
        apiUrl = "http://gaiadev3.systematrix.ai/external_link/" + inputValue + "/party";
    }
  
    // Open the URL in a new tab
    window.open(apiUrl, '_blank');
});
  
function retrieveRecentImage(documentType) {
    $.ajax({
        url: `/retrieve_recent_image/${documentType}/`,
        type: 'GET',
        success: function(data) {
            // Update the href attribute of the anchor tag
            $('#recentImageLink').attr('href', data);
        },
        error: function(xhr, status, error) {
            console.error(error);
            alert('No recent image found');
        }
    });
}
  
// New JavaScript code to handle form submission and display success message

// document.addEventListener('DOMContentLoaded', function() {
//     const form = document.querySelector(form[action="{% url 'save_application' %}"]);
//     form.addEventListener('submit', function(event) {
//         event.preventDefault();  // Prevent default form submission

//         const formData = new FormData(form);
//         const submitButton = form.querySelector('input[type="submit"]');
//         submitButton.disabled = true;  // Disable the submit button to prevent multiple submissions

//         fetch(form.action, {
//             method: 'POST',
//             body: formData,
//             headers: {
//                 'X-CSRFToken': form.querySelector('input[name="csrfmiddlewaretoken"]').value
//             }
//         })
//         .then(response => response.json())
//         .then(data => {
//             submitButton.disabled = false;  // Re-enable the submit button
//             const messageDiv = document.getElementById('messageDiv');
//             messageDiv.textContent = `Record ${data.unique_id} created and stored`;
//             messageDiv.style.color = 'green';
//         })
//         .catch(error => {
//             submitButton.disabled = false;  // Re-enable the submit button
//             const messageDiv = document.getElementById('messageDiv');
//             messageDiv.textContent = 'An error occurred. Please try again.';
//             messageDiv.style.color = 'red';
//         });
//     });
// });

// document.getElementById('uploadForm').addEventListener('submit', function() {
//     document.getElementById('loading-spinner').style.display = 'block';
// });