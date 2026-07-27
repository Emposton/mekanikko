const { useState } = React;

function MekanikkoGame() {
  const [money, setMoney] = useState(500);
  const [reputation, setReputation] = useState(1);
  const [carState, setCarState] = useState({
    cvt: "Vinkuu kovilla kierroksilla",
    brakes: "Pehmeä poljin, vähän tehoa",
    lights: "Takavalossa kosketushäiriö",
    oil: "Öljy tummaa, ei kriittinen"
  });
  const [log, setLog] = useState([
    "Tervetuloa mopoautokorjaamoon – ensimmäinen asiakas odottaa!"
  ]);

  function addLog(msg) {
    setLog(prev => [msg, ...prev].slice(0, 20));
  }

  function diagnose(part) {
    switch (part) {
      case "cvt":
        addLog("Diagnostiikka: CVT-hihna kulunut, kotelo likainen.");
        break;
      case "brakes":
        addLog("Diagnostiikka: Jarruneste vanhaa, takasylinteri vähän jumissa.");
        break;
      case "lights":
        addLog("Diagnostiikka: Maadoitus huono, liitin hapettunut.");
        break;
      case "oil":
        addLog("Diagnostiikka: Öljynvaihto suositeltu, ei pakollinen.");
        break;
      default:
        addLog("Diagnostiikka: Ei valittua osaa.");
    }
  }

  function repair(part) {
    if (money < 50) {
      addLog("Ei tarpeeksi rahaa korjaukseen.");
      return;
    }

    setMoney(money - 50);
    setReputation(reputation + 0.1);

    switch (part) {
      case "cvt":
        setCarState(s => ({ ...s, cvt: "CVT toimii pehmeästi, ei vinkunaa." }));
        addLog("Korjaus: Vaihdettiin CVT-hihna ja puhdistettiin kotelo.");
        break;
      case "brakes":
        setCarState(s => ({ ...s, brakes: "Jarrut terävät ja tasaiset." }));
        addLog("Korjaus: Vaihdettiin jarruneste ja herkistettiin takasylinteri.");
        break;
      case "lights":
        setCarState(s => ({ ...s, lights: "Kaikki valot toimivat moitteetta." }));
        addLog("Korjaus: Puhdistettiin liittimet ja parannettiin maadoitus.");
        break;
      case "oil":
        setCarState(s => ({ ...s, oil: "Tuore öljy, moottori käy nätisti." }));
        addLog("Korjaus: Öljynvaihto tehty.");
        break;
      default:
        addLog("Korjaus: Ei valittua osaa.");
    }
  }

  function testDrive() {
    addLog("Testiajo: Mopoauto kiihtyy tasaisesti, ei ylimääräisiä ääniä.");
    setMoney(money + 80);
    setReputation(reputation + 0.2);
  }

  return (
    React.createElement("div", { className: "game-container" },
      React.createElement("div", { className: "header" },
        React.createElement("div", null,
          React.createElement("h2", null, "Mekanikko – Superpeli"),
          React.createElement("p", null, "Korjaa mopoauto, pidä maine ja rahat tasapainossa.")
        ),
        React.createElement("div", null,
          React.createElement("p", null, `Rahat: €${money.toFixed(0)}`),
          React.createElement("p", null, `Maine: ${reputation.toFixed(1)} / 5`)
        )
      ),
      React.createElement("div", { className: "garage-view" },
        React.createElement("div", { className: "car-panel" },
          React.createElement("h3", null, "Mopoauto korjaamolla"),
          React.createElement("p", null, "CVT: ", carState.cvt),
          React.createElement("p", null, "Jarrut: ", carState.brakes),
          React.createElement("p", null, "Valot: ", carState.lights),
          React.createElement("p", null, "Öljy: ", carState.oil),
          React.createElement("div", { className: "button-row" },
            React.createElement("button", { onClick: () => diagnose("cvt") }, "Diagnosoi CVT"),
            React.createElement("button", { onClick: () => diagnose("brakes") }, "Diagnosoi jarrut"),
            React.createElement("button", { onClick: () => diagnose("lights") }, "Diagnosoi valot"),
            React.createElement("button", { onClick: () => diagnose("oil") }, "Diagnosoi öljy")
          )
        ),
        React.createElement("div", { className: "actions-panel" },
          React.createElement("h3", null, "Toiminnot"),
          React.createElement("div", { className: "button-row" },
            React.createElement("button", { onClick: () => repair("cvt") }, "Korjaa CVT"),
            React.createElement("button", { onClick: () => repair("brakes") }, "Korjaa jarrut"),
            React.createElement("button", { onClick: () => repair("lights") }, "Korjaa valot"),
            React.createElement("button", { onClick: () => repair("oil") }, "Vaihda öljy"),
            React.createElement("button", { onClick: testDrive }, "Testiajo ja luovutus")
          ),
          React.createElement("div", { className: "log" },
            log.map((entry, i) =>
              React.createElement("div", { key: i }, "• ", entry)
            )
          )
        )
      )
    )
  );
}

ReactDOM.createRoot(document.getElementById("root")).render(
  React.createElement(MekanikkoGame)
);
