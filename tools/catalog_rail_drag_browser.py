"""Focused browser checks for mouse dragging on horizontal catalog rails."""
import asyncio
import json
from pathlib import Path

from playwright.async_api import async_playwright

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "assets" / "catalog-rail-drag.js"
REPORT = ROOT / ".local" / "catalog-rail-drag-result.json"

HTML = """
<!doctype html>
<html>
<head>
  <style>
    body { min-height: 1400px; margin: 0; padding: 48px; }
    .catalog-rail {
      display: flex; width: 420px; height: 140px; gap: 12px;
      overflow-x: auto; overflow-y: hidden; scroll-snap-type: x proximity;
    }
    .shelf-card { flex: 0 0 180px; height: 120px; scroll-snap-align: start; }
    .catalog-rail--dragging { scroll-snap-type: none; }
  </style>
</head>
<body>
  <div id="rail" class="catalog-rail" role="region" aria-label="Filmes">
    <button id="card-1" class="shelf-card" type="button">
      <img id="poster" draggable="true" alt="" src="data:image/gif;base64,R0lGODlhAQABAAD/ACwAAAAAAQABAAACADs=">
      Filme 1
    </button>
    <button id="card-2" class="shelf-card" type="button">Filme 2</button>
    <button id="card-3" class="shelf-card" type="button">Filme 3</button>
    <button id="card-4" class="shelf-card" type="button">Filme 4</button>
  </div>
  <button id="outside" type="button">Controle fora da prateleira</button>
  <div id="short-rail" class="catalog-rail">
    <button id="short-card" class="shelf-card" type="button">Único filme</button>
  </div>
  <script>
    window.openedCards = 0;
    window.clickLog = [];
    window.captureCalls = 0;
    window.loadMoreEvents = 0;
    const rail = document.querySelector('#rail');
    rail.addEventListener('scroll', () => {
      if (rail.scrollLeft + rail.clientWidth >= rail.scrollWidth - 240) {
        window.loadMoreEvents += 1;
      }
    });
    document.addEventListener('click', event => {
      window.clickLog.push({
        target: event.target.id,
        detail: event.detail,
        pointerId: event.pointerId
      });
      if (event.target.closest('.shelf-card')) window.openedCards += 1;
    });
    const capture = Element.prototype.setPointerCapture;
    Element.prototype.setPointerCapture = function(...args) {
      window.captureCalls += 1;
      return capture.apply(this, args);
    };
  </script>
</body>
</html>
"""


async def run():
    report = {
        "passed": False,
        "cases": [],
        "unexpected_requests": [],
        "unexpected_websockets": [],
    }
    async with async_playwright() as pw:
        browser = await pw.chromium.launch(channel="msedge", headless=True)
        try:
            page = await browser.new_page(viewport={"width": 900, "height": 700})
            page.on(
                "request",
                lambda request: report["unexpected_requests"].append(request.url),
            )
            page.on(
                "websocket",
                lambda socket: report["unexpected_websockets"].append(socket.url),
            )
            await page.set_content(HTML)
            await page.add_script_tag(path=str(SCRIPT))
            await page.add_script_tag(path=str(SCRIPT))
            rail = page.locator("#rail")
            bounds = await rail.bounding_box()
            y = bounds["y"] + bounds["height"] / 2

            await page.mouse.move(bounds["x"] + 340, y)
            await page.mouse.down()
            await page.mouse.move(bounds["x"] + 100, y, steps=6)
            dragstart_allowed = await page.evaluate(
                """() => {
                  const event = new DragEvent('dragstart', {bubbles: true, cancelable: true});
                  document.querySelector('#poster').dispatchEvent(event);
                  return !event.defaultPrevented;
                }"""
            )
            assert not dragstart_allowed
            await page.mouse.up()
            scroll_after_drag = await rail.evaluate("(node) => node.scrollLeft")
            assert scroll_after_drag > 100, scroll_after_drag
            await page.wait_for_timeout(50)
            assert await page.evaluate("window.loadMoreEvents") > 0
            assert await page.evaluate("window.openedCards") == 0
            assert await page.evaluate("window.captureCalls") == 1
            assert "catalog-rail--dragging" not in (await rail.get_attribute("class"))
            report["cases"].append(
                {
                    "horizontal_drag_moves_content": True,
                    "drag_does_not_activate_card": True,
                    "native_image_drag_does_not_interrupt": True,
                    "single_capture_after_duplicate_script_load": True,
                    "drag_state_cleaned_on_pointerup": True,
                    "native_scroll_event_reaches_load_more_threshold": True,
                }
            )

            await rail.evaluate("(node) => { node.scrollLeft = 0; }")
            bounds = await rail.bounding_box()
            y = bounds["y"] + bounds["height"] / 2
            await page.mouse.move(bounds["x"] + 340, y)
            await page.mouse.down()
            await page.mouse.move(bounds["x"] + 340, y + 30, steps=3)
            await page.mouse.up()
            assert await rail.evaluate("(node) => node.scrollLeft") == 0
            assert await page.evaluate("window.openedCards") == 0
            assert "catalog-rail--dragging" not in (await rail.get_attribute("class"))
            report["cases"].append(
                {
                    "vertical_intent_does_not_drag_shelf": True,
                    "vertical_intent_does_not_activate_card": True,
                }
            )

            await rail.evaluate("(node) => { node.scrollLeft = 0; }")
            first = page.locator("#card-1")
            first_bounds = await first.bounding_box()
            click_y = first_bounds["y"] + first_bounds["height"] / 2
            click_x = first_bounds["x"] + first_bounds["width"] / 2
            await page.mouse.move(click_x, click_y)
            await page.mouse.down()
            await page.mouse.move(click_x + 3, click_y, steps=1)
            await page.mouse.up()
            opened = await page.evaluate("window.openedCards")
            assert opened == 1, await page.evaluate("window.clickLog")
            await first.focus()
            await page.keyboard.press("Enter")
            assert await page.evaluate("window.openedCards") == 2
            report["cases"].append(
                {
                    "subthreshold_click_opens_card": True,
                    "keyboard_activation_opens_card": True,
                }
            )

            await rail.evaluate("(node) => { node.scrollLeft = 0; }")
            bounds = await rail.bounding_box()
            y = bounds["y"] + bounds["height"] / 2
            await page.mouse.move(bounds["x"] + 340, y)
            await page.mouse.down()
            await page.mouse.move(bounds["x"] + 100, y, steps=6)
            await page.mouse.up()
            await page.wait_for_timeout(20)
            await first.click()
            assert await page.evaluate("window.openedCards") == 3
            report["cases"].append({"later_click_not_suppressed": True})

            bounds = await rail.bounding_box()
            y = bounds["y"] + bounds["height"] / 2
            await page.mouse.move(bounds["x"] + 340, y)
            await page.mouse.down()
            await page.mouse.move(bounds["x"] + 100, y, steps=6)
            await page.evaluate(
                """() => document.querySelector('#rail').dispatchEvent(
                  new PointerEvent('pointercancel', {
                    bubbles: true, pointerId: 1, pointerType: 'mouse'
                  })
                )"""
            )
            assert "catalog-rail--dragging" not in (await rail.get_attribute("class"))
            await page.mouse.up()
            report["cases"].append({"pointer_cancel_cleans_drag_state": True})

            short_rail = page.locator("#short-rail")
            short_bounds = await short_rail.bounding_box()
            await page.mouse.move(short_bounds["x"] + 30, short_bounds["y"] + 30)
            await page.mouse.down()
            await page.mouse.move(short_bounds["x"] + 5, short_bounds["y"] + 30, steps=3)
            await page.mouse.up()
            assert await short_rail.evaluate("(node) => node.scrollLeft") == 0
            report["cases"].append({"no_overflow_rail_not_moved": True})

            await rail.evaluate("(node) => { node.scrollLeft = 0; }")
            bounds = await rail.bounding_box()
            y = bounds["y"] + bounds["height"] / 2
            await page.mouse.move(bounds["x"] + 180, y)
            await page.mouse.wheel(240, 0)
            await page.wait_for_timeout(50)
            assert await rail.evaluate("(node) => node.scrollLeft") > 0
            report["cases"].append({"native_horizontal_wheel_remains_available": True})

            await page.mouse.move(bounds["x"] + 180, y)
            await page.mouse.wheel(0, 300)
            await page.wait_for_timeout(100)
            vertical_scroll = await page.evaluate("window.scrollY")
            assert vertical_scroll > 0, {
                "scrollY": vertical_scroll,
                "bodyHeight": await page.locator("body").evaluate("(node) => node.scrollHeight"),
                "pointer": await page.evaluate("({x: window.event?.clientX, y: window.event?.clientY})"),
            }
            report["cases"].append({"vertical_wheel_remains_native": True})

            old_scroll = await rail.evaluate("(node) => node.scrollLeft")
            await page.evaluate(
                """() => {
                  const rail = document.querySelector('#rail');
                  const options = {
                    bubbles: true, pointerId: 7, pointerType: 'touch',
                    isPrimary: true, button: 0, clientX: 300, clientY: 100
                  };
                  rail.dispatchEvent(new PointerEvent('pointerdown', options));
                  rail.dispatchEvent(new PointerEvent('pointermove', {
                    ...options, clientX: 100
                  }));
                  rail.dispatchEvent(new PointerEvent('pointerup', options));
                }"""
            )
            assert await rail.evaluate("(node) => node.scrollLeft") == old_scroll
            assert "catalog-rail--dragging" not in (await rail.get_attribute("class"))
            assert await rail.evaluate("(node) => getComputedStyle(node).touchAction") == "auto"
            report["cases"].append({"touch_input_not_intercepted": True})

            assert not report["unexpected_requests"], report["unexpected_requests"]
            assert not report["unexpected_websockets"], report["unexpected_websockets"]
            report["passed"] = True
        finally:
            await browser.close()
            REPORT.parent.mkdir(parents=True, exist_ok=True)
            REPORT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report))


if __name__ == "__main__":
    asyncio.run(run())
