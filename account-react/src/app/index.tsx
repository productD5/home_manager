import { AppRouter } from "./router";
import { AppProvider } from "./provider";

export const App = () => {
  return (
    <AppProvider>
      <AppRouter />
    </AppProvider>
  );
};
