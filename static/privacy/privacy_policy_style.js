window.onscroll = function() {
    scrollFunction();
  };
  
function scrollFunction() {
    if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
        document.getElementById("scrollTopBtn").classList.add("show");
    } else {
        document.getElementById("scrollTopBtn").classList.remove("show");
    }
}
  
function scrollToTop() {
document.body.scrollTop = 0;
document.documentElement.scrollTop = 0;
}