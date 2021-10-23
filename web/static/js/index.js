function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

async function load() {
	for (i = 1; i < 65; i ++ ) {
		let pic = document.getElementById('pic' + i);
    	pic.style.opacity = 1;
    	await sleep(300 - Math.sqrt(i)*30);
	}
	await sleep(500);
	let bg = document.getElementById('landing-wrapper');
	bg.style.opacity = .9;
}

document.addEventListener("DOMContentLoaded", (event) => {
	
    load();
});
