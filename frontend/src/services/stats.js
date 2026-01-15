import { api } from "./api";

export async function getStatsOverview() {
  const { data } = await api.get("/stats/overview");
  return data;
}
