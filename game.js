const { useState, useEffect, useRef } = React;

function MekanikkoGame() {
  const [money, setMoney] = useState(500);
  const [reputation, setReputation] = useState(1.0);
  const [log, setLog] = useState([
    "Tervetuloa pseudo-3D mopoautokorjaamoon!"
  ]);
  const [selectedPart, setSelectedPart] = useState(null);
  const canvasRef = useRef(null);

  const parts = useRef([
    { id: "cvt", x: 260, y: 190, w: 80, h: 40, color: "#f97316", state: "kiinni" },
    { id: "brakes", x: 180, y: 230, w: 60, h: 30, color: "#22c55e", state: "kulunut" },
    { id: "lights", x: 360, y: 170, w: 40, h: 25, color: "#eab308", state: "pätkii" },
    { id: "oil", x: 310, y: 140, w: 30, h: 30, color: "#0ea5e9", state: "tumma" }
  ]);

  const dragState = useRef({
    dragging: false,
    partId: null,
    offsetX: 0,
    offsetY: 0
  });

  function addLog(msg) {
    setLog(prev => [msg, ...prev].slice(0, 25));
  }

  function drawScene(ctx) {
    ctx.clearRect(0, 0, ctx.canvas.width, ctx.canvas.height);

    // pseudo-3D lattia
    ctx.fillStyle = "#111";
    ctx.fillRect(0, 260, 600, 140);
    ctx.fillStyle = "#1f2937";
    ctx.beginPath();
    ctx.moveTo(0, 260);
    ctx.lineTo(600, 260);
    ctx.lineTo(600, 240);
    ctx.lineTo(0, 240);
    ctx.closePath();
    ctx.fill();

    // auto (runko)
    ctx.fillStyle = "#6b7280";
    ctx.fillRect(150, 180, 260, 70);
    ctx.fillStyle = "#9ca3af";
    ctx.fillRect(190, 150, 180, 40);

    // renkaat
    ctx.fillStyle = "#000";
    ctx.beginPath();
    ctx.arc(190, 250, 22, 0, Math.PI * 2);
    ctx.arc(340, 250, 22, 0, Math.PI * 2);
    ctx.fill();

    // osat (placeholder-3D)
    parts.current.forEach(p => {
      ctx.fillStyle = p.color;
      ctx.fillRect(p.x, p.y, p.w, p.h);
      ctx.fillStyle = "#000";
      ctx.font = "10px system-ui";
      ctx.fillText(p.id.toUpperCase(), p.x + 4, p.y + 12);
    });
  }

  useEffect(() => {
    const canvas = canvasRef.current;
    const ctx = canvas.getContext("2d");
    drawScene(ctx);

    function getPartAt(x, y) {
      return parts.current.find(
        p => x >= p.x && x <= p.x + p.w && y >= p.y && y <= p.y + p.h
      );
    }

    function onMouseDown(e) {
      const rect = canvas.getBoundingClientRect();
      const x = e.clientX - rect.left;
      const y = e.clientY - rect.top;
      const part = getPartAt(x, y);
      if (part) {
        dragState.current.dragging = true;
        dragState.current.partId = part.id;
        dragState.current.offsetX = x - part.x;
        dragState.current.offsetY = y - part.y;
        setSelectedPart(part.id);
        addLog(`Valitsit osan: ${part.id.toUpperCase()}`);
      }
    }

    function onMouseMove(e) {
      if (!dragState.current.dragging) return;
      const rect = canvas.getBoundingClientRect();
      const x = e.clientX - rect.left;
      const y = e.clientY - rect.top;
      const part = parts.current.find(p => p.id === dragState.current.partId);
      if (part) {
        part.x = x - dragState.current.offsetX;
        part.y = y - dragState.current.offsetY;
        drawScene(ctx);
      }
    }

    function onMouseUp() {
      dragState.current.dragging = false;
      dragState.current.partId = null;
    }

    canvas.addEventListener("mousedown", onMouseDown);
    window.addEventListener("mousemove", onMouseMove);
    window.addEventListener("mouseup", onMouseUp);

    return () => {
      canvas.removeEventListener("mousedown", onMouseDown);
      window.removeEventListener("mousemove", onMouseMove);
      window.removeEventListener("mouseup", onMouseUp);
    };
  }, []);

  function repairSelected() {
    if (!selectedPart) {
      addLog("Valitse ensin osa canvasista.");
      return;
    }
    if (money < 50) {
      addLog("Ei tarpeeksi rahaa korjaukseen.");
      return;
    }
    setMoney(m => m - 50);
    setReputation(r => r + 0.2);

    const part = parts.current.find(p => p.id === selectedPart);
    if (part) {
      part.state = "kunnossa";
      part.color = "#22c55e";
      addLog(`Korjasit osan: ${selectedPart.toUpperCase()}`);
      const ctx = canvasRef.current.getContext("2d");
      drawScene(ctx);
    }
  }

  function testDrive() {
    addLog("Testiajo: auto kiihtyy, tarkistetaan korjatut osat...");
    const allGood = parts.current.every(p => p.state === "kunnossa");
    if (allGood) {
      addLog("Testiajo: kaikki kunnossa, asiakas tyytyväinen!");
      setMoney(m => m + 120);
      setReputation(r => Math.min(5, r + 0.5));
    } else {
      addLog("Testiajo: jokin osa vielä pielessä, asiakas ei täysin tyytyväinen.");
      setReputation(r => Math.max(0, r - 0.2));
    }
  }

  return React.createElement(
    "div",
    { className: "game-container" },
    React.createElement(
      "div",
      { className: "canvas-wrapper" },
      React.createElement("h3", null, "Mopoauto – pseudo 3D näkymä"),
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
      React.createElement("p", null, `Rahat: €${money.toFixed(0)}`),
      React.createElement("p", null, `Maine: ${reputation.toFixed(1)} / 5`),
      React.createElement(
        "p",
        null,
        selectedPart
          ? `Valittu osa: ${selectedPart.toUpperCase()}`
          : "Valitse osa klikkaamalla canvasia."
      ),
      React.createElement(
        "button",
        { onClick: repairSelected },
        "Korjaa valittu osa"
      ),
      React.createElement(
        "button",
        { onClick: testDrive },
        "Testiajo"
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
