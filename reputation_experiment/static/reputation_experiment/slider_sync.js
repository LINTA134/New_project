/* === slider_sync.js (スライダーの数値連動スクリプト) === */

/**
 * スライダーの現在値を横のテキストにリアルタイムで同期させる関数
 * @param {string} sliderSelector - 対象スライダーのCSSセレクタ (例: '.invest-slider')
 * @param {string} valueDisplaySelector - 数値表示用spanのCSSセレクタ (例: '.slider-value')
 */
window.setupSliderSync = function(sliderSelector, valueDisplaySelector) {
  document.querySelectorAll(sliderSelector).forEach(slider => {
    const container = slider.closest('.slider-container');
    if (!container) return;
    const valueDisplay = container.querySelector(valueDisplaySelector);
    if (!valueDisplay) return;

    // 初期値設定
    valueDisplay.textContent = slider.value;

    // inputイベントで値を更新
    slider.addEventListener('input', () => {
      valueDisplay.textContent = slider.value;
    });
  });
};

/* --- ページ読み込み時に実行 --- */
document.addEventListener("DOMContentLoaded", function() {
    // 投資額スライダーの連動を初期化
    if (window.setupSliderSync) {
        window.setupSliderSync('.invest-slider', '.slider-value');
    }
});