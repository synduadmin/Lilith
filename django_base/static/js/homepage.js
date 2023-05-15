            /*
            var observer = new IntersectionObserver(function(entries) {
                console.log('observing')
            entries.forEach(function(entry) {
                if (entry.isIntersecting) {
                var img = entry.target;
                img.src = img.dataset.src;
                observer.unobserve(img);
                }
            });
            });

            var lazyPixelatedImages = document.querySelectorAll('.lazy-pixelated');
            lazyPixelatedImages.forEach(function(img) {
                console.log('registering observing')

            observer.observe(img);


            });*/

            function animateMoon() {
                const moon = document.getElementById("moon");
                const scene = document.getElementById("main_scene");
                const interval = parseFloat(moon.dataset.interval);
                let xPos = scene.clientHeight / 4;
                let yPos = scene.clientHeight;
                const endY = 0 - 3*moon.clientHeight;

                function moveMoon() {
                    xPos += 0.05 * interval;
                    yPos -= interval;
                    moon.style.transform = `translate(${xPos}px, ${yPos}px)`;
                    if (yPos > endY) {
                        window.requestAnimationFrame(moveMoon);
                    } else {
                        moon.style.transform = `translate(${xPos}px, ${endY}px)`;
                        yPos = scene.clientHeight + moon.clientHeight
                        setTimeout(() => {
                            moon.remove();
                        }, 10000); // remove moon after 1 second
                    }
                }

                window.requestAnimationFrame(moveMoon);

            }
            //animateMoon();

            function animateCloud(num) {
                let cloudName = 'cloud'+num;
                const cloud = document.getElementById(cloudName);
                const interval = parseFloat(cloud.dataset.interval);
                const scene = document.getElementById("main_scene");
                let xPos = 0 - cloud.clientWidth;
                let yPos = cloud.offsetTop;
                const endX = scene.clientWidth + 2 * cloud.clientWidth;

                function moveCloud() {
                    xPos += interval;
                    yPos = yPos;
                    cloud.style.transform = `translate(${xPos}px, ${yPos}px)`;
                    if (xPos < endX) {
                        window.requestAnimationFrame(moveCloud);
                    } else {
                        cloud.style.transform = `translate(${endX}px, ${yPos}px)`;
                        //cloud.style.opacity = 0;
                        setTimeout(() => {
                            xPos = 0 - 1.5*cloud.clientWidth;
                            window.requestAnimationFrame(moveCloud);

                        }, 1000); // remove moon after 1 second
                    }
                }

                window.requestAnimationFrame(moveCloud);

            }

        animateMoon();
        animateCloud(1);
        animateCloud(2);
        animateCloud(3);
        animateCloud(4);
        animateCloud(5);
        animateCloud(6);
