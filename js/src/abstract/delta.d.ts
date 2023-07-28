import { implicitReturnType } from '../base/types.js';
import { Exchange as _Exchange } from '../base/Exchange.js';
interface Exchange {
    publicGetAssets(params?: {}): Promise<implicitReturnType>;
    publicGetIndices(params?: {}): Promise<implicitReturnType>;
    publicGetProducts(params?: {}): Promise<implicitReturnType>;
    publicGetProductsSymbol(params?: {}): Promise<implicitReturnType>;
    publicGetTickers(params?: {}): Promise<implicitReturnType>;
    publicGetTickersSymbol(params?: {}): Promise<implicitReturnType>;
    publicGetL2orderbookSymbol(params?: {}): Promise<implicitReturnType>;
    publicGetTradesSymbol(params?: {}): Promise<implicitReturnType>;
    publicGetStats(params?: {}): Promise<implicitReturnType>;
    publicGetHistoryCandles(params?: {}): Promise<implicitReturnType>;
    publicGetHistorySparklines(params?: {}): Promise<implicitReturnType>;
    publicGetSettings(params?: {}): Promise<implicitReturnType>;
    privateGetOrders(params?: {}): Promise<implicitReturnType>;
    privateGetProductsProductIdOrdersLeverage(params?: {}): Promise<implicitReturnType>;
    privateGetPositionsMargined(params?: {}): Promise<implicitReturnType>;
    privateGetPositions(params?: {}): Promise<implicitReturnType>;
    privateGetOrdersHistory(params?: {}): Promise<implicitReturnType>;
    privateGetFills(params?: {}): Promise<implicitReturnType>;
    privateGetFillsHistoryDownloadCsv(params?: {}): Promise<implicitReturnType>;
    privateGetWalletBalances(params?: {}): Promise<implicitReturnType>;
    privateGetWalletTransactions(params?: {}): Promise<implicitReturnType>;
    privateGetWalletTransactionsDownload(params?: {}): Promise<implicitReturnType>;
    privateGetWalletsSubAccountsTransferHistory(params?: {}): Promise<implicitReturnType>;
    privateGetUsersTradingPreferences(params?: {}): Promise<implicitReturnType>;
    privateGetSubAccounts(params?: {}): Promise<implicitReturnType>;
    privateGetProfile(params?: {}): Promise<implicitReturnType>;
    privateGetDepositsAddress(params?: {}): Promise<implicitReturnType>;
    privateGetOrdersLeverage(params?: {}): Promise<implicitReturnType>;
    privatePostOrders(params?: {}): Promise<implicitReturnType>;
    privatePostOrdersBracket(params?: {}): Promise<implicitReturnType>;
    privatePostOrdersBatch(params?: {}): Promise<implicitReturnType>;
    privatePostProductsProductIdOrdersLeverage(params?: {}): Promise<implicitReturnType>;
    privatePostPositionsChangeMargin(params?: {}): Promise<implicitReturnType>;
    privatePostPositionsCloseAll(params?: {}): Promise<implicitReturnType>;
    privatePostWalletsSubAccountBalanceTransfer(params?: {}): Promise<implicitReturnType>;
    privatePostOrdersCancelAfter(params?: {}): Promise<implicitReturnType>;
    privatePostOrdersLeverage(params?: {}): Promise<implicitReturnType>;
    privatePutOrders(params?: {}): Promise<implicitReturnType>;
    privatePutOrdersBracket(params?: {}): Promise<implicitReturnType>;
    privatePutOrdersBatch(params?: {}): Promise<implicitReturnType>;
    privatePutPositionsAutoTopup(params?: {}): Promise<implicitReturnType>;
    privatePutUsersUpdateMmp(params?: {}): Promise<implicitReturnType>;
    privatePutUsersResetMmp(params?: {}): Promise<implicitReturnType>;
    privateDeleteOrders(params?: {}): Promise<implicitReturnType>;
    privateDeleteOrdersAll(params?: {}): Promise<implicitReturnType>;
    privateDeleteOrdersBatch(params?: {}): Promise<implicitReturnType>;
}
declare abstract class Exchange extends _Exchange {
}
export default Exchange;
