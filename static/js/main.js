function next(el, slider, onChange) {
  const inner = el.querySelector(".inner");
  const input = inner.querySelector("input");

  if (input) {
    inner.insertAdjacentHTML(
      "beforeend",
      `
<div class="btn-container">
    <button class="btn prev">Prev</button>
    <button class="btn next">Next</button>
</div>
    `
    );

    const nextBtn = inner.querySelector(".btn.next");
    const prevBtn = inner.querySelector(".btn.prev");

    slider.subscribe(() => {
      if (slider.hasPrev()) {
        prevBtn.classList.add("show");
      }
    });

    prevBtn.onclick = e => {
      e.preventDefault();
      e.stopImmediatePropagation();

      slider.prev();
    };

    nextBtn.onclick = e => {
      e.preventDefault();
      e.stopImmediatePropagation();

      slider.next();
    };

    input.addEventListener("input", e => {
      if (input.value) {
        nextBtn.classList.add("show");
      } else {
        nextBtn.classList.remove("show");
      }
    });
  }
}

function createSlider(panels) {
  let index = -1;
  const lastIndex = panels.length - 1;
  const listeners = [];
  const indexes = new Array(panels.length - 1).fill(false);

  function animate(index) {
    if (index !== lastIndex) listeners[index]();

    panels[index].querySelector("h1").style.opacity = 1;

    if (!indexes[index]) {
      const splitTitle = new SplitText(panels[index].querySelector("h1"), {
        type: "chars"
      });
      const titleChars = splitTitle.chars;
      indexes[index] = titleChars;
    }

    const x = index * -windowWidth;

    const timeline = new TimelineMax({ onComplete });

    function onComplete() {
      if (index === lastIndex) {
        const form = document.forms[0];
        form.submit();
      }
    }

    timeline
      .to("#main", 1, {
        x,
        ease: Power3.easeInOut
      })
      .staggerFromTo(
        indexes[index],
        1,
        {
          opacity: 0,
          y: "100%"
        },
        {
          opacity: 1,
          y: "0%",
          ease: Power3.easeInOut
        },
        0.1,
        "-=1"
      );
  }

  return {
    subscribe(cb) {
      listeners.push(cb);
    },
    hasPrev() {
      return index - 1 >= 0;
    },
    hasNext() {
      return index + 1 <= lastIndex;
    },
    prev() {
      animate((index = Math.max(--index, 0)));
    },
    next() {
      animate((index = Math.min(++index, lastIndex)));
    }
  };
}

function init(slider) {
  const splitTitle = new SplitText("#title", { type: "chars" });
  const titleChars = splitTitle.chars;

  const preloaderTimeline = new TimelineMax({
    onComplete() {
      slider.next();
    }
  });
  TweenMax.set("#title", { perspective: 400 });

  preloaderTimeline
    .staggerFrom(
      titleChars,
      1,
      {
        opacity: 0,
        y: "100%",
        transformOrigin: "0% 50% -50",
        ease: Back.easeOut
      },
      0.1
    )

    .staggerTo(
      ["#preloader", "#main"],
      2,
      {
        cycle: {
          y: ["-100%", "0%"]
        },
        ease: Power3.easeOut
      },
      0
    )
    .to(
      "#preloader",
      3,
      {
        backgroundColor: "#a13939",
        ease: Power3.easeInOut
      },
      "0"
    );
}

const windowWidth = window.innerWidth;
const panels = document.querySelectorAll(".panel");

const slider = createSlider(panels);
for (let i = 0; i < panels.length; ++i) {
  const panel = panels[i];
  next(panel, slider);
  TweenMax.set(panel, {
    x: i * windowWidth
  });
}

// Don't submit on when you press enter.
window.addEventListener("keydown", e => {
  const ENTER = 13;

  if (e.keyCode === ENTER) {
    e.preventDefault();
    slider.next();
  }
});

init(slider);
