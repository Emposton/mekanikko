const { useState, useEffect, useRef } = React;

function MekanikkoGame() {
  const [money, setMoney] = useState(500);
  const [reputation, setReputation] = useState(1.0);
  const [log, setLog] = useState(["Pseudo‑3D korjaamo käynnissä"]);
  const [selectedPart, setSelectedPart] = useState(null);

  const canvasRef = useRef(null);

  // zoom & pan
  const view = useRef({
    zoom: 1.0,
    offsetX: 0,
    offsetY: 0,
    dragging: false,
    dragStartX: 0,
    dragStartY: 0
  });

  // placeholder‑kuvat
  const images = useRef({
    car: new Image(),
    cvt: new Image(),
    brakes: new Image(),
    lights: new Image(),
    oil: new Image()
  });

 images.current.car.src = "images/mauto.jpg";
images.current.cvt.src = "images/cvt.webp";
images.current.brakes.src = "images/jarru.webp";
images.current.lights.src = "images/valo.jpg";
images.current.oil.src = "images/oljy.webp";


  const parts = useRef([
    { id: "cvt", x: 260, y: 190, w: 80, h: 40, img: "cvt", state: "kiinni" },
    { id: "brakes", x: 180, y: 230, w: 60, h: 30, img: "brakes", state: "kulunut" },
    { id: "lights", x: 360, y: 170, w: 40, h: 25, img: "lights", state: "pätkii" },
    { id: "oil", x: 310, y: 140, w: 30, h: 30, img: "oil", state: "tumma" }
  ]);

  function addLog(msg) {
    setLog(prev => [msg, ...prev].slice(0, 25));
  }

  function drawScene(ctx) {
    ctx.clearRect(0, 0, ctx.canvas.width, ctx.canvas.height);

    ctx.save();
    ctx.translate(view.current.offsetX, view.current.offsetY);
    ctx.scale(view.current.zoom, view.current.zoom);

    // auto
    ctx.drawImage(images.current.car, 100, 100, 400, 200);

    // osat
    parts.current.forEach(p => {
      const img = images.current[p.img];
      ctx.drawImage(img, p.x, p.y, p.w, p.h);
    });

    ctx.restore();
  }

  useEffect(() => {
    const canvas = canvasRef.current;
    const ctx = canvas.getContext("2d");

    function redraw() {
      drawScene(ctx);
    }

    redraw();

    // zoom
    canvas.addEventListener("wheel", e => {
      e.preventDefault();
      const delta = e.deltaY > 0 ? -0.1 : 0.1;
      view.current.zoom = Math.max(0.5, Math.min(2.5, view.current.zoom + delta));
      redraw();
    });

    // pan
    canvas.addEventListener("mousedown", e => {
      view.current.dragging = true;
      view.current.dragStartX = e.clientX - view.current.offsetX;
      view.current.dragStartY = e.clientY - view.current.offsetY;
    });

    window.addEventListener("mousemove", e => {
      if (!view.current.dragging) return;
      view.current.offsetX = e.clientX - view.current.dragStartX;
      view.current.offsetY = e.clientY - view.current.dragStartY;
      redraw();
    });

    window.addEventListener("mouseup", () => {
      view.current.dragging = false;
    });

    // osien valinta
    canvas.addEventListener("click", e => {
      const rect = canvas.getBoundingClientRect();
      const x = (e.clientX - rect.left - view.current.offsetX) / view.current.zoom;
      const y = (e.clientY - rect.top - view.current.offsetY) / view.current.zoom;

      const part = parts.current.find(
        p => x >= p.x && x <= p.x + p.w && y >= p.y && y <= p.h + p.y
      );

      if (part) {
        setSelectedPart(part.id);
        addLog(`Valitsit osan: ${part.id.toUpperCase()}`);
      }
    });
  }, []);

  function repairSelected() {
    if (!selectedPart) {
      addLog("Valitse osa ensin.");
      return;
    }

    const part = parts.current.find(p => p.id === selectedPart);
    part.state = "kunnossa";

    addLog(`Korjasit osan: ${selectedPart.toUpperCase()}`);

    setMoney(m => m - 50);
    setReputation(r => r + 0.2);

    drawScene(canvasRef.current.getContext("2d"));
  }

  return React.createElement(
    "div",
    { className: "game-container" },
    React.createElement(
      "div",
      { className: "canvas-wrapper" },
      React.createElement("h3", null, "Pseudo‑3D mopoauto"),
      React.createElement("canvas", {
        ref: canvasRef,
        width: 600,
        height: 400
      })
    ),
    React.createElement(
      "div",
      { className: "side-panel" },
      React.createElement("h3", null, "Korjauspaneeli"),
      React.createElement("p", null, `Rahat: €${money}`),
      React.createElement("p", null, `Maine: ${reputation.toFixed(1)} / 5`),
      React.createElement(
        "p",
        null,
        selectedPart ? `Valittu osa: ${selectedPart}` : "Ei valittua osaa"
      ),
      React.createElement(
        "button",
        { onClick: repairSelected },
        "Korjaa osa"
      ),
      React.createElement(
        "div",
        { className: "log" },
        log.map((entry, i) =>
          React.createElement("div", { key: i }, "• ", entry)
        )
      )
    )
  );
}

ReactDOM.createRoot(document.getElementById("root")).render(
  React.createElement(MekanikkoGame)
);
