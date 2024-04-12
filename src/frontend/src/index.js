import { createRoot } from "react-dom/client";
import App from "./App";

if (module.hot) {
    module.hot.accept();
}

const root = createRoot(document.querySelector("#root"));

root.render(<App />);
