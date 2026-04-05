 if (window.AOS && typeof window.AOS.init === 'function') {
	AOS.init({
		duration: 800,
		easing: 'slide'
	});
 }

var initThemeToggle = function() {
	var toggle = document.getElementById('theme-toggle');
	if (!toggle) {
		return;
	}
	var themeKey = 'pypass-theme';
	var body = document.body;
	var applyTheme = function(theme) {
		body.classList.remove('theme-light', 'theme-dark');
		body.classList.add(theme);
		toggle.setAttribute('data-theme', theme);
	};
	var stored;
	try {
		stored = localStorage.getItem(themeKey);
	} catch (error) {
		stored = null;
	}
	if (!stored) {
		stored = window.matchMedia('(prefers-color-scheme: dark)').matches
			? 'theme-dark'
			: 'theme-light';
	}
	applyTheme(stored);
	toggle.addEventListener('click', function() {
		var next = body.classList.contains('theme-dark') ? 'theme-light' : 'theme-dark';
		applyTheme(next);
		try {
			localStorage.setItem(themeKey, next);
		} catch (error) {
			// Ignore storage failures (private mode or blocked storage).
		}
	});
};

if (document.readyState === 'loading') {
	document.addEventListener('DOMContentLoaded', initThemeToggle);
} else {
	initThemeToggle();
}

$(document).ready(function($) {

	"use strict";

	// Stellar parallax disabled to avoid getClientRects errors in modern layouts.


	var hideLoader = function() {
		var loaderEl = document.getElementById('ftco-loader');
		if (!loaderEl) {
			return;
		}
		loaderEl.classList.remove('show');
		loaderEl.style.display = 'none';
	};

	// loader
	var loader = function() {
		setTimeout(function() {
			if (window.jQuery && $('#ftco-loader').length > 0) {
				$('#ftco-loader').removeClass('show');
			} else {
				hideLoader();
			}
		}, 1);
	};
	loader();
	window.addEventListener('load', hideLoader);
	document.addEventListener('DOMContentLoaded', hideLoader);

	var updateLdapStatus = function() {
		var statusEl = document.getElementById('ldap-status');
		if (!statusEl) {
			return;
		}
		var endpoint = statusEl.getAttribute('data-endpoint');
		fetch(endpoint, { cache: 'no-store' })
			.then(function(response) {
				return response.json();
			})
			.then(function(payload) {
				if (payload && payload.ok) {
					statusEl.classList.remove('ldap-fail', 'ldap-unknown');
					statusEl.classList.add('ldap-ok');
				} else {
					statusEl.classList.remove('ldap-ok', 'ldap-unknown');
					statusEl.classList.add('ldap-fail');
				}
			})
			.catch(function() {
				statusEl.classList.remove('ldap-ok', 'ldap-unknown');
				statusEl.classList.add('ldap-fail');
			});
	};
	updateLdapStatus();
	setInterval(updateLdapStatus, 30000);

	var carousel = function() {
		$('.carousel').owlCarousel({
			loop: false,
			items:1,
			margin: 30,
			stagePadding: 0,
			nav: false,
			navText: ['<span class="icon-arrow_back">', '<span class="icon-arrow_forward">'],
			responsive:{
				0:{
					items: 1
				},
				600:{
					items: 2
				},
				1000:{
					items: 3
				}
			}
		});

		// $('.nonloop').owlCarousel({
	 //    center: true,
	 //    items:1,
	 //    loop:false,
	 //    margin:10,
	 //    nav: true,
		// 	navText: ['<span class="icon-arrow_back">', '<span class="icon-arrow_forward">'],
	 //    responsive:{
	 //    	0:{
		// 	 items: 1
		// 	},
  //        600:{
  //         items:2
  //        },
  //        1000:{
		// 	 items: 3
		//    }
	 //    }
		// });
	};
	carousel();

	// scroll
	var scrollWindow = function() {
		if (window.matchMedia('(max-width: 1024px)').matches) {
			return;
		}
		$(window).scroll(function(){
			var $w = $(this),
					st = $w.scrollTop(),
					navbar = $('.ftco_navbar'),
					sd = $('.js-scroll-wrap');

			if (st > 150) {
				if ( !navbar.hasClass('scrolled') ) {
					navbar.addClass('scrolled');	
				}
			} 
			if (st < 150) {
				if ( navbar.hasClass('scrolled') ) {
					navbar.removeClass('scrolled sleep');
				}
			} 
			if ( st > 350 ) {
				if ( !navbar.hasClass('awake') ) {
					navbar.addClass('awake');	
				}
				
				if(sd.length > 0) {
					sd.addClass('sleep');
				}
			}
			if ( st < 350 ) {
				if ( navbar.hasClass('awake') ) {
					navbar.removeClass('awake');
					navbar.addClass('sleep');
				}
				if(sd.length > 0) {
					sd.removeClass('sleep');
				}
			}
		});
	};
	scrollWindow();

	var isMobile = {
		Android: function() {
			return navigator.userAgent.match(/Android/i);
		},
			BlackBerry: function() {
			return navigator.userAgent.match(/BlackBerry/i);
		},
			iOS: function() {
			return navigator.userAgent.match(/iPhone|iPad|iPod/i);
		},
			Opera: function() {
			return navigator.userAgent.match(/Opera Mini/i);
		},
			Windows: function() {
			return navigator.userAgent.match(/IEMobile/i);
		},
			any: function() {
			return (isMobile.Android() || isMobile.BlackBerry() || isMobile.iOS() || isMobile.Opera() || isMobile.Windows());
		}
	};

	var mobileMenuOutsideClick = function() {

		$(document).click(function (e) {
	    var container = $("#colorlib-offcanvas, .js-colorlib-nav-toggle");
	    if (!container.is(e.target) && container.has(e.target).length === 0) {

	    	if ( $('body').hasClass('offcanvas') ) {

    			$('body').removeClass('offcanvas');
    			$('.js-colorlib-nav-toggle').removeClass('active');
				
	    	}
	    
	    	
	    }
		});

	};
	mobileMenuOutsideClick();


	var offcanvasMenu = function() {

		$('#page').prepend('<div id="colorlib-offcanvas" />');
		$('#page').prepend('<a href="#" class="js-colorlib-nav-toggle colorlib-nav-toggle colorlib-nav-white"><i></i></a>');
		var clone1 = $('.menu-1 > ul').clone();
		$('#colorlib-offcanvas').append(clone1);
		var clone2 = $('.menu-2 > ul').clone();
		$('#colorlib-offcanvas').append(clone2);

		$('#colorlib-offcanvas .has-dropdown').addClass('offcanvas-has-dropdown');
		$('#colorlib-offcanvas')
			.find('li')
			.removeClass('has-dropdown');

		// Hover dropdown menu on mobile
		$('.offcanvas-has-dropdown').mouseenter(function(){
			var $this = $(this);

			$this
				.addClass('active')
				.find('ul')
				.slideDown(500, 'easeOutExpo');				
		}).mouseleave(function(){

			var $this = $(this);
			$this
				.removeClass('active')
				.find('ul')
				.slideUp(500, 'easeOutExpo');				
		});


		$(window).resize(function(){

			if ( $('body').hasClass('offcanvas') ) {

    			$('body').removeClass('offcanvas');
    			$('.js-colorlib-nav-toggle').removeClass('active');
				
	    	}
		});
	};
	offcanvasMenu();


	var burgerMenu = function() {

		$('body').on('click', '.js-colorlib-nav-toggle', function(event){
			var $this = $(this);


			if ( $('body').hasClass('overflow offcanvas') ) {
				$('body').removeClass('overflow offcanvas');
			} else {
				$('body').addClass('overflow offcanvas');
			}
			$this.toggleClass('active');
			event.preventDefault();

		});
	};
	burgerMenu();
	
	var counter = function() {
		
		$('#section-counter').waypoint( function( direction ) {

			if( direction === 'down' && !$(this.element).hasClass('ftco-animated') ) {

				var comma_separator_number_step = $.animateNumber.numberStepFactories.separator(',')
				$('.number').each(function(){
					var $this = $(this),
						num = $this.data('number');
						console.log(num);
					$this.animateNumber(
					  {
					    number: num,
					    numberStep: comma_separator_number_step
					  }, 7000
					);
				});
				
			}

		} , { offset: '95%' } );

	}
	counter();

	var contentWayPoint = function() {
		var i = 0;
		$('.ftco-animate').waypoint( function( direction ) {

			if( direction === 'down' && !$(this.element).hasClass('ftco-animated') ) {
				
				i++;

				$(this.element).addClass('item-animate');
				setTimeout(function(){

					$('body .ftco-animate.item-animate').each(function(k){
						var el = $(this);
						setTimeout( function () {
							var effect = el.data('animate-effect');
							if ( effect === 'fadeIn') {
								el.addClass('fadeIn ftco-animated');
							} else if ( effect === 'fadeInLeft') {
								el.addClass('fadeInLeft ftco-animated');
							} else if ( effect === 'fadeInRight') {
								el.addClass('fadeInRight ftco-animated');
							} else {
								el.addClass('fadeInUp ftco-animated');
							}
							el.removeClass('item-animate');
						},  k * 50, 'easeInOutExpo' );
					});
					
				}, 100);
				
			}

		} , { offset: '95%' } );
	};
	contentWayPoint();


	// navigation
	var OnePageNav = function() {
		$(".smoothscroll[href^='#'], #ftco-nav ul li a[href^='#']").on('click', function(e) {
		 	e.preventDefault();

		 	var hash = this.hash,
		 			navToggler = $('.navbar-toggler');
		 	$('html, body').animate({
		    scrollTop: $(hash).offset().top
		  }, 700, 'easeInOutExpo', function(){
		    window.location.hash = hash;
		  });


		  if ( navToggler.is(':visible') ) {
		  	navToggler.click();
		  }
		});
		$('body').on('activate.bs.scrollspy', function () {
		  console.log('nice');
		})
	};
	OnePageNav();


	// magnific popup
	$('.image-popup').magnificPopup({
    type: 'image',
    closeOnContentClick: true,
    closeBtnInside: false,
    fixedContentPos: true,
    mainClass: 'mfp-no-margins mfp-with-zoom', // class to remove default margin from left and right side
     gallery: {
      enabled: true,
      navigateByImgClick: true,
      preload: [0,1] // Will preload 0 - before current, and 1 after the current image
    },
    image: {
      verticalFit: true
    },
    zoom: {
      enabled: true,
      duration: 300 // don't foget to change the duration also in CSS
    }
  });

  $('.popup-youtube, .popup-vimeo, .popup-gmaps').magnificPopup({
          disableOn: 700,
          type: 'iframe',
          mainClass: 'mfp-fade',
          removalDelay: 160,
          preloader: false,

          fixedContentPos: false
        });

 //  $('#m_date').datepicker({
	//   'format': 'm/d/yyyy',
	//   'autoclose': true
	// });
	// $('#m_time').timepicker();



});

