export const paths = {
  Welcome: {
    path: "/",
    getHref: () => "/",
  },
  Login: {
    path: "/login",
    getHref: () => "/login",
  },
  sign_up: {
    path: "/sign-up",
    getHref: () => "/sign-up",
  },
  home: {
    path: "/home",
    getHref: () => "/home",
  },
} as const;
