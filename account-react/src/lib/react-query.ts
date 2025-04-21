import { UseMutationOptions, DefaultOptions } from '@tanstack/react-query';

// queryConfigの設定
export const queryConfig: DefaultOptions = {
  queries: {
    refetchOnWindowFocus: false,  // ウィンドウがフォーカスされても再フェッチしない
    retry: false,  // クエリが失敗した場合に再試行しない
    staleTime: 1000 * 60,  // データが古いと見なされる時間を1分に設定
  },
};

// API関数の戻り値の型を取得するユーティリティ型
export type ApiFnReturnType<FnType extends (...args: any) => Promise<any>> =
  Awaited<ReturnType<FnType>>;

// クエリの設定を取得する型（queryKey と queryFn を除く）
export type QueryConfig<T extends (...args: any[]) => any> = Omit<
  ReturnType<T>,
  'queryKey' | 'queryFn'
>;

// ミューテーションの設定を取得する型
export type MutationConfig<MutationFnType extends (...args: any) => Promise<any>> =
  UseMutationOptions<
    ApiFnReturnType<MutationFnType>,  // ミューテーションの戻り値の型
    Error,  // エラー型
    Parameters<MutationFnType>[0]  // 引数の最初の型（通常はリクエストボディ）
  >;
