import { Exchange } from './base/Exchange.js';
export default class stex extends Exchange {
    describe(): any;
    fetchCurrencies(params?: {}): Promise<{}>;
    fetchMarkets(params?: {}): Promise<any[]>;
    fetchTicker(symbol: any, params?: {}): Promise<import("./base/types.js").Ticker>;
    fetchTime(params?: {}): Promise<number>;
    fetchOrderBook(symbol: any, limit?: any, params?: {}): Promise<import("./base/types.js").OrderBook>;
    parseTicker(ticker: any, market?: any): import("./base/types.js").Ticker;
    fetchTickers(symbols?: string[], params?: {}): Promise<any>;
    parseOHLCV(ohlcv: any, market?: any): number[];
    fetchOHLCV(symbol: any, timeframe?: string, since?: any, limit?: any, params?: {}): Promise<import("./base/types.js").OHLCV[]>;
    parseTrade(trade: any, market?: any): import("./base/types.js").Trade;
    fetchTrades(symbol: any, since?: any, limit?: any, params?: {}): Promise<import("./base/types.js").Trade[]>;
    fetchTradingFee(symbol: any, params?: {}): Promise<{
        info: any;
        symbol: any;
        maker: number;
        taker: number;
        percentage: boolean;
        tierBased: boolean;
    }>;
    parseBalance(response: any): import("./base/types.js").Balances;
    fetchBalance(params?: {}): Promise<import("./base/types.js").Balances>;
    parseOrderStatus(status: any): string;
    parseOrder(order: any, market?: any): any;
    createOrder(symbol: any, type: any, side: any, amount: any, price?: any, params?: {}): Promise<any>;
    fetchOrder(id: any, symbol?: string, params?: {}): Promise<any>;
    fetchClosedOrder(id: any, symbol?: string, params?: {}): Promise<any>;
    fetchOrderTrades(id: any, symbol?: string, since?: any, limit?: any, params?: {}): Promise<any>;
    fetchOpenOrders(symbol?: string, since?: any, limit?: any, params?: {}): Promise<import("./base/types.js").Order[]>;
    cancelOrder(id: any, symbol?: string, params?: {}): Promise<any>;
    cancelAllOrders(symbol?: string, params?: {}): Promise<any>;
    fetchMyTrades(symbol?: string, since?: any, limit?: any, params?: {}): Promise<import("./base/types.js").Trade[]>;
    createDepositAddress(code: any, params?: {}): Promise<{
        currency: any;
        address: string;
        tag: string;
        info: any;
    }>;
    fetchDepositAddress(code: any, params?: {}): Promise<{
        currency: any;
        address: string;
        tag: string;
        network: any;
        info: any;
    }>;
    sign(path: any, api?: any, method?: string, params?: {}, headers?: any, body?: any): {
        url: string;
        method: string;
        body: any;
        headers: any;
    };
    parseTransactionStatus(status: any): string;
    parseTransaction(transaction: any, currency?: any): {
        info: any;
        id: string;
        txid: string;
        timestamp: number;
        datetime: string;
        network: string;
        addressFrom: any;
        address: string;
        addressTo: string;
        tagFrom: any;
        tag: string;
        tagTo: string;
        type: string;
        amount: number;
        currency: any;
        status: string;
        updated: number;
        fee: any;
    };
    fetchDeposit(id: any, code?: any, params?: {}): Promise<{
        info: any;
        id: string;
        txid: string;
        timestamp: number;
        datetime: string;
        network: string;
        addressFrom: any;
        address: string;
        addressTo: string;
        tagFrom: any;
        tag: string;
        tagTo: string;
        type: string;
        amount: number;
        currency: any;
        status: string;
        updated: number;
        fee: any;
    }>;
    fetchDeposits(code?: string, since?: any, limit?: any, params?: {}): Promise<any>;
    fetchWithdrawal(id: any, code?: any, params?: {}): Promise<{
        info: any;
        id: string;
        txid: string;
        timestamp: number;
        datetime: string;
        network: string;
        addressFrom: any;
        address: string;
        addressTo: string;
        tagFrom: any;
        tag: string;
        tagTo: string;
        type: string;
        amount: number;
        currency: any;
        status: string;
        updated: number;
        fee: any;
    }>;
    fetchWithdrawals(code?: string, since?: any, limit?: any, params?: {}): Promise<any>;
    transfer(code: any, amount: any, fromAccount: any, toAccount: any, params?: {}): Promise<{
        info: any;
        id: string;
        timestamp: any;
        datetime: any;
        currency: any;
        amount: any;
        fromAccount: any;
        toAccount: any;
        status: any;
    }>;
    parseTransfer(transfer: any, currency?: any): {
        info: any;
        id: string;
        timestamp: any;
        datetime: any;
        currency: any;
        amount: any;
        fromAccount: any;
        toAccount: any;
        status: any;
    };
    withdraw(code: any, amount: any, address: any, tag?: any, params?: {}): Promise<{
        info: any;
        id: string;
        txid: string;
        timestamp: number;
        datetime: string;
        network: string;
        addressFrom: any;
        address: string;
        addressTo: string;
        tagFrom: any;
        tag: string;
        tagTo: string;
        type: string;
        amount: number;
        currency: any;
        status: string;
        updated: number;
        fee: any;
    }>;
    fetchTransactionFees(codes?: string[], params?: {}): Promise<{}>;
    fetchDepositWithdrawFees(codes?: string[], params?: {}): Promise<{}>;
    parseDepositWithdrawFee(fee: any, currency?: any): {
        withdraw: {
            fee: number;
            percentage: boolean;
        };
        deposit: {
            fee: number;
            percentage: boolean;
        };
        networks: {};
    };
    handleErrors(httpCode: any, reason: any, url: any, method: any, headers: any, body: any, response: any, requestHeaders: any, requestBody: any): void;
}
