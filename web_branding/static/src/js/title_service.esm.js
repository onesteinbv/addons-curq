import {registry} from "@web/core/registry";

// For a lack of a better way to customize this we need to override the whole service
export const titleService = {
    start() {
        const titleCounters = {};
        const titleParts = {};

        function getParts() {
            return Object.assign({}, titleParts);
        }

        function updateTitle() {
            const counter = Object.values(titleCounters).reduce(
                (acc, count) => acc + count,
                0
            );
            const name = Object.values(titleParts).join(" - ") || "CURQ";
            if (counter) {
                document.title = `(${counter}) ${name}`;
            } else {
                document.title = name;
            }
        }

        function setCounters(counters) {
            for (const key in counters) {
                const val = counters[key];
                if (val) {
                    titleCounters[key] = val;
                } else {
                    delete titleCounters[key];
                }
            }
            updateTitle();
        }

        function setParts(parts) {
            for (const key in parts) {
                const val = parts[key];
                if (val) {
                    titleParts[key] = val;
                } else {
                    delete titleParts[key];
                }
            }
            updateTitle();
        }

        return {
            /**
             * @returns {String}
             */
            get current() {
                return document.title;
            },
            getParts,
            setCounters,
            setParts,
        };
    },
};

registry.category("services").remove("title");
registry.category("services").add("title", titleService);
