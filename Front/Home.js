var animateHTML = function() {
    var elems;
    var windowHeight;

    function init() {
      elems = document.querySelectorAll('.animated-card');
      windowHeight = window.innerHeight;
      addEventHandlers();
      updateOnPosition();
    }
    
    function addEventHandlers() {
      window.addEventListener('scroll', updateOnPosition);
      window.addEventListener('resize', init);
    }

    function updateOnPosition() {
      for (var i = 0; i < elems.length; i++) {
        var positionFromTop = elems[i].getBoundingClientRect().top;
        if (positionFromTop - windowHeight <= 0) {
          elems[i].className = elems[i].className.replace(
            'animated-card',
            'slide-in-bottom-animation'
          );    
        }
      }
    }

    return {
      init: init
    };
  };
  animateHTML().init();