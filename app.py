
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="반응속도 테스트",
    layout="wide"
)

html_code = r"""

<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>반응속도 테스트</title>

  <style>
    * {
      box-sizing: border-box;
    }

    body {
      margin: 0;
      font-family: Arial, sans-serif;
      text-align: center;
      background-color: #f5f5f5;
    }

    h1 {
      margin-top: 30px;
    }

    .container {
      position: relative;
      display: flex;
      justify-content: center;
      align-items: center;
      width: 100%;
      min-height: 450px;
      margin: 25px auto;
    }

    .game-area {
      width: 90%;
      max-width: 700px;
      text-align: center;
    }

    #game {
      width: 100%;
      height: 350px;
      margin: 0 auto 25px;
      background-color: #d93636;
      color: white;
      display: flex;
      justify-content: center;
      align-items: center;
      font-size: 32px;
      font-weight: bold;
      cursor: pointer;
      border-radius: 15px;
      user-select: none;
    }

    #game.green {
      background-color: #16a34a;
    }

    button {
      padding: 12px 30px;
      font-size: 18px;
      border: none;
      border-radius: 8px;
      background-color: #333333;
      color: white;
      cursor: pointer;
    }

    button:disabled {
      background-color: #999999;
      cursor: not-allowed;
    }

    #results {
      position: absolute;
      left: calc(50% + 380px);
      top: 50%;
      transform: translateY(-50%);
      width: 220px;
      min-width: 180px;
      padding: 20px;
      background-color: white;
      border-radius: 12px;
      font-size: 18px;
      line-height: 1.8;
      text-align: left;
    }

    #results h2 {
      font-size: 21px;
    }

    @media (max-width: 1100px) {
      .container {
        flex-direction: column;
        gap: 25px;
      }

      .game-area {
        width: 90%;
      }

      #results {
        position: static;
        transform: none;
        width: 90%;
        max-width: 700px;
      }
    }
  </style>
</head>

<body>

  <h1>반응속도 테스트</h1>
  <p>초록색으로 바뀌면 최대한 빠르게 클릭하세요!</p>

  <div class="container">

    <div class="game-area">
      <div id="game">시작 버튼을 누르세요</div>
      <button id="startBtn">시작</button>
    </div>

    <div id="results">
      <p>반응속도 기록이 여기에 표시됩니다.</p>
    </div>

  </div>

  <script>
    const game = document.querySelector("#game");
    const startBtn = document.querySelector("#startBtn");
    const results = document.querySelector("#results");

    let count = 0;
    let times = [];
    let startTime = 0;
    let timer;
    let phase = "ready";

    startBtn.addEventListener("click", startGame);

    function startGame() {
      clearTimeout(timer);

      count = 0;
      times = [];
      phase = "countdown";

      startBtn.disabled = true;
      results.innerHTML = "<p>반응속도 측정 중...</p>";

      countdown(3);
    }

    function countdown(number) {
      game.classList.remove("green");
      game.textContent = number;

      if (number > 1) {
        timer = setTimeout(function() {
          countdown(number - 1);
        }, 1000);
      } else {
        timer = setTimeout(function() {
          startRound();
        }, 1000);
      }
    }

    function startRound() {
      phase = "waiting";
      game.classList.remove("green");
      game.textContent = "";

      const randomTime = 2000 + Math.random() * 3000;

      timer = setTimeout(function() {
        phase = "green";
        game.classList.add("green");
        game.textContent = "";
        startTime = performance.now();
      }, randomTime);
    }

    game.addEventListener("click", function() {
      if (phase === "waiting") {
        clearTimeout(timer);
        phase = "falseStart";
        game.textContent = "너무 빨라요! 다시 시도하세요.";

        timer = setTimeout(function() {
          startRound();
        }, 1000);

      } else if (phase === "green") {
        const reactionTime = performance.now() - startTime;

        times.push(reactionTime);
        count++;

        phase = "recorded";
        game.textContent =
          (reactionTime / 1000).toFixed(3) + "초";

        updateResults();

        timer = setTimeout(function() {
          game.classList.remove("green");

          if (count < 3) {
            startRound();
          } else {
            finishGame();
          }
        }, 2000);
      }
    });

    function updateResults() {
      results.innerHTML = "<h3>반응속도 기록</h3>";

      for (let i = 0; i < times.length; i++) {
        results.innerHTML +=
          "<p>" + (i + 1) + "회차: " +
          (times[i] / 1000).toFixed(3) +
          "초</p>";
      }
    }

    function finishGame() {
      phase = "finished";

      const total = times.reduce(function(sum, time) {
        return sum + time;
      }, 0);

      const average = total / times.length;

      game.classList.add("green");
      game.textContent = "테스트 완료!";

      results.innerHTML +=
        "<h2>평균: " +
        (average / 1000).toFixed(3) +
        "초</h2>";

      startBtn.disabled = false;
      startBtn.textContent = "다시 시작";
    }
  </script>

</body>
</html>

"""

components.html(
    html_code,
    height=650,
    scrolling=True
)
