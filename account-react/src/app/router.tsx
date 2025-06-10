import { useMemo } from "react";
import { paths } from "../config/paths";

import { QueryClient, useQueryClient } from "@tanstack/react-query";
import { createBrowserRouter } from "react-router";
import { RouterProvider } from "react-router-dom";
import { Spinner } from "../components/ui/spinner";

const convert = (queryClient: QueryClient) => (m: any) => {
  const { clientLoader, clientAction, default: Component, ...rest } = m;
  return {
    ...rest,
    loader: clientLoader?.(queryClient),
    action: clientAction?.(queryClient),
    Component,
  };
};

const createAppRouter = (queryClient: QueryClient) =>
  createBrowserRouter([
    {
      path: paths.Login.path,
      hydrateFallbackElement: <Spinner />,
      lazy: () => import("./routes/login").then(convert(queryClient)),
    },
    {
      path: paths.sign_up.path,
      hydrateFallbackElement: <Spinner />,
      lazy: () => import("./routes/signup").then(convert(queryClient)),
    },
    {
      path: paths.Welcome.path,
      hydrateFallbackElement: <Spinner />,
      lazy: () => import("./routes/welcome").then(convert(queryClient)),
    },
    {
      path: paths.home.path,
      hydrateFallbackElement: <Spinner />,
      lazy: () => import("./routes/app/home").then(convert(queryClient)),
    },
    {
      path: "*",
      lazy: () => import("./routes/not-found").then(convert(queryClient)),
    },
  ]);

export const AppRouter = () => {
  const queryClient = useQueryClient();

  const router = useMemo(() => createAppRouter(queryClient), [queryClient]);

  return <RouterProvider router={router} />;
};
