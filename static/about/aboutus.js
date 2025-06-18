// window.onscroll = function() {
//     scrollFunction();
//   };
  
// function scrollFunction() {
//     if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
//         document.getElementById("scrollTopBtn").classList.add("show");
//     } else {
//         document.getElementById("scrollTopBtn").classList.remove("show");
//     }
// }
  
// function scrollToTop() {
// document.body.scrollTop = 0;
// document.documentElement.scrollTop = 0;
// }

let observer = new IntersectionObserver((e)=>{
    e.forEach((박스)=>{
        if (박스.isIntersecting){
            박스.target.style.opacity = 1;
            박스.target.style.transform = 'rotate(0deg)';
        } 
        
    })
})
let div = document.querySelectorAll('div')
observer.observe(div[0])
observer.observe(div[1])
observer.observe(div[2])
observer.observe(div[3])