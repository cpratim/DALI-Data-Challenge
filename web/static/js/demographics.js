
document.addEventListener("DOMContentLoaded", async (event) => {
	
    let response = await fetch('/get_demographics')
    
	let json = await response.json();
	console.log(json);
    
    var barColors = [
	  "#b91d47",
	  "#00aba9",
	  "#2b5797",
	  "#e8c3b9",
	  "#1e7145", 
	  "#00548B",
	  "#9B00B3",
	  "#A9CB00",
	  "#91FFAF",
	  "#E50063",
	];
    for (let chart in json) {
    	let dataPoints = []
	    let labels = []
	    for (let key in json[chart]) {
	    	dataPoints.push(json[chart][key])
	    	labels.push(key)
	    }
	    new Chart("pie-chart-" + chart , {
		  type: "pie",
		  data: {
		    labels: labels,
		    datasets: [{
		      backgroundColor: barColors,
		      data: dataPoints,
		    }]
		  },
		  options: {
		  	legend: {
			    display: true,
			    position: "top",
			    labels: {
			      fontColor: "white",
			      fontSize: 16
			    }
			},
		  }
		  

		}); 
    }
    

});
