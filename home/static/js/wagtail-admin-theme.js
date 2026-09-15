/*
 * Progressive enhancement for the admin theme's status badges.
 *
 * Wagtail only distinguishes "live" (w-status--primary) from everything
 * else at the CSS level -- draft, scheduled, and expired all render as
 * the same plain .w-status. The badge text itself ("live", "draft",
 * "scheduled", "expired", "live + draft", "live + scheduled") is the
 * only place the distinction shows up, so this reads that text once
 * and records it as a data attribute for wagtail-admin-theme.css to
 * key off. If this script fails to run for any reason, the badges
 * simply keep the baseline live/draft coloring already defined in CSS
 * -- nothing here is required for the page to work.
 */
(function () {
    "use strict";

    var SCOPE_SELECTOR = ".listing-page .w-status, .listing.full-width .w-status";

    function classify(el) {
        var text = el.textContent.trim().toLowerCase();
        var hasLive = text.indexOf("live") !== -1;
        var hasDraft = text.indexOf("draft") !== -1;
        var kind = null;

        if (text.indexOf("expired") !== -1) {
            kind = "expired";
        } else if (text.indexOf("scheduled") !== -1 && !hasLive) {
            kind = "scheduled";
        } else if (hasLive && hasDraft) {
            kind = "live-draft";
        } else if (hasLive) {
            kind = "live";
        } else if (hasDraft) {
            kind = "draft";
        }

        if (!kind) return;
        el.dataset.wStatusKind = kind;

        if (kind === "live-draft" && !el.querySelector(".w-status-substatus")) {
            var dot = document.createElement("span");
            dot.className = "w-status-substatus";
            dot.setAttribute("aria-hidden", "true");
            dot.title = "Has unpublished changes";
            el.appendChild(dot);
        }
    }

    function enhance() {
        document.querySelectorAll(SCOPE_SELECTOR).forEach(classify);
    }

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", enhance);
    } else {
        enhance();
    }
})();
