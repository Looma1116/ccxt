import { Exchange } from './base/Exchange.js';
export default class binance extends Exchange {
    describe(): any;
    isInverse(type: any, subType?: any): boolean;
    isLinear(type: any, subType?: any): boolean;
    setSandboxMode(enable: any): void;
    convertExpireDate(date: any): string;
    createExpiredOptionMarket(symbol: any): {
        id: string;
        symbol: string;
        base: any;
        quote: string;
        baseId: any;
        quoteId: string;
        active: any;
        type: string;
        linear: any;
        inverse: any;
        spot: boolean;
        swap: boolean;
        future: boolean;
        option: boolean;
        margin: boolean;
        contract: boolean;
        contractSize: any;
        expiry: number;
        expiryDatetime: string;
        optionType: string;
        strike: string;
        settle: string;
        settleId: string;
        precision: {
            amount: any;
            price: any;
        };
        limits: {
            amount: {
                min: any;
                max: any;
            };
            price: {
                min: any;
                max: any;
            };
            cost: {
                min: any;
                max: any;
            };
        };
        info: any;
    };
    market(symbol: any): any;
    safeMarket(marketId?: any, market?: any, delimiter?: any, marketType?: any): any;
    costToPrecision(symbol: any, cost: any): any;
    currencyToPrecision(code: any, fee: any, networkCode?: any): any;
    nonce(): number;
    fetchTime(params?: {}): Promise<number>;
    fetchCurrencies(params?: {}): Promise<{}>;
    fetchMarkets(params?: {}): Promise<any[]>;
    parseMarket(market: any): {
        id: string;
        lowercaseId: string;
        symbol: string;
        base: any;
        quote: any;
        settle: any;
        baseId: string;
        quoteId: string;
        settleId: string;
        type: any;
        spot: boolean;
        margin: any;
        swap: boolean;
        future: boolean;
        option: boolean;
        active: boolean;
        contract: boolean;
        linear: any;
        inverse: any;
        taker: any;
        maker: any;
        contractSize: any;
        expiry: number;
        expiryDatetime: string;
        strike: number;
        optionType: string;
        precision: {
            amount: number;
            price: number;
            base: number;
            quote: number;
        };
        limits: {
            leverage: {
                min: any;
                max: any;
            };
            amount: {
                min: number;
                max: number;
            };
            price: {
                min: any;
                max: any;
            };
            cost: {
                min: any;
                max: any;
            };
        };
        info: any;
    };
    parseBalanceHelper(entry: any): import("./base/types.js").Balance;
    parseBalance(response: any, type?: any, marginMode?: any): {
        info: any;
    };
    fetchBalance(params?: {}): Promise<{
        info: any;
    }>;
    fetchOrderBook(symbol: any, limit?: any, params?: {}): Promise<import("./base/types.js").OrderBook>;
    parseTicker(ticker: any, market?: any): import("./base/types.js").Ticker;
    fetchStatus(params?: {}): Promise<{
        status: string;
        updated: any;
        eta: any;
        url: any;
        info: any;
    }>;
    fetchTicker(symbol: any, params?: {}): Promise<import("./base/types.js").Ticker>;
    fetchBidsAsks(symbols?: string[], params?: {}): Promise<any>;
    fetchLastPrices(symbols?: string[], params?: {}): Promise<any>;
    parseLastPrice(info: any, market?: any): {
        symbol: any;
        timestamp: number;
        datetime: string;
        price: number;
        side: any;
        baseVolume: any;
        quoteVolume: any;
        info: any;
    };
    fetchTickers(symbols?: string[], params?: {}): Promise<any>;
    parseOHLCV(ohlcv: any, market?: any): number[];
    fetchOHLCV(symbol: any, timeframe?: string, since?: any, limit?: any, params?: {}): Promise<import("./base/types.js").OHLCV[]>;
    parseTrade(trade: any, market?: any): import("./base/types.js").Trade | {
        id: any;
        timestamp: number;
        datetime: string;
        symbol: any;
        order: string;
        type: any;
        takerOrMaker: any;
        side: any;
        amount: number;
        price: number;
        cost: number;
        fee: {
            currency: any;
            cost: number;
        };
        info: any;
    };
    fetchTrades(symbol: any, since?: any, limit?: any, params?: {}): Promise<import("./base/types.js").Trade[]>;
    editOrder(id: any, symbol: any, type: any, side: any, amount: any, price?: any, params?: {}): Promise<any>;
    parseOrderStatus(status: any): string;
    parseOrder(order: any, market?: any): any;
    createOrder(symbol: any, type: any, side: any, amount: any, price?: any, params?: {}): Promise<any>;
    fetchOrder(id: any, symbol?: string, params?: {}): Promise<any>;
    fetchOrders(symbol?: string, since?: any, limit?: any, params?: {}): Promise<import("./base/types.js").Order[]>;
    fetchOpenOrders(symbol?: string, since?: any, limit?: any, params?: {}): Promise<import("./base/types.js").Order[]>;
    fetchClosedOrders(symbol?: string, since?: any, limit?: any, params?: {}): Promise<any[]>;
    cancelOrder(id: any, symbol?: string, params?: {}): Promise<any>;
    cancelAllOrders(symbol?: string, params?: {}): Promise<any>;
    fetchOrderTrades(id: any, symbol?: string, since?: any, limit?: any, params?: {}): Promise<import("./base/types.js").Trade[]>;
    fetchMyTrades(symbol?: string, since?: any, limit?: any, params?: {}): Promise<import("./base/types.js").Trade[]>;
    fetchMyDustTrades(symbol?: string, since?: any, limit?: any, params?: {}): Promise<any>;
    parseDustTrade(trade: any, market?: any): {
        id: any;
        timestamp: number;
        datetime: string;
        symbol: any;
        order: string;
        type: any;
        takerOrMaker: any;
        side: any;
        amount: number;
        price: number;
        cost: number;
        fee: {
            currency: any;
            cost: number;
        };
        info: any;
    };
    fetchDeposits(code?: string, since?: any, limit?: any, params?: {}): Promise<any>;
    fetchWithdrawals(code?: string, since?: any, limit?: any, params?: {}): Promise<any>;
    parseTransactionStatusByType(status: any, type?: any): string;
    parseTransaction(transaction: any, currency?: any): {
        info: any;
        id: string;
        txid: string;
        timestamp: any;
        datetime: string;
        network: string;
        address: string;
        addressTo: string;
        addressFrom: any;
        tag: string;
        tagTo: string;
        tagFrom: any;
        type: string;
        amount: number;
        currency: any;
        status: string;
        updated: number;
        internal: number;
        fee: any;
    };
    parseTransferStatus(status: any): string;
    parseTransfer(transfer: any, currency?: any): {
        info: any;
        id: string;
        timestamp: number;
        datetime: string;
        currency: any;
        amount: number;
        fromAccount: any;
        toAccount: any;
        status: string;
    };
    parseIncome(income: any, market?: any): {
        info: any;
        symbol: any;
        code: any;
        timestamp: number;
        datetime: string;
        id: string;
        amount: number;
    };
    transfer(code: any, amount: any, fromAccount: any, toAccount: any, params?: {}): Promise<{
        info: any;
        id: string;
        timestamp: number;
        datetime: string;
        currency: any;
        amount: number;
        fromAccount: any;
        toAccount: any;
        status: string;
    }>;
    fetchTransfers(code?: string, since?: any, limit?: any, params?: {}): Promise<any>;
    fetchDepositAddress(code: any, params?: {}): Promise<{
        currency: any;
        address: string;
        tag: string;
        network: any;
        info: any;
    }>;
    fetchTransactionFees(codes?: string[], params?: {}): Promise<{
        withdraw: {};
        deposit: {};
        info: any;
    }>;
    fetchDepositWithdrawFees(codes?: string[], params?: {}): Promise<{}>;
    parseDepositWithdrawFee(fee: any, currency?: any): {
        info: any;
        withdraw: {
            fee: any;
            percentage: any;
        };
        deposit: {
            fee: any;
            percentage: any;
        };
        networks: {};
    };
    withdraw(code: any, amount: any, address: any, tag?: any, params?: {}): Promise<{
        info: any;
        id: string;
        txid: string;
        timestamp: any;
        datetime: string;
        network: string;
        address: string;
        addressTo: string;
        addressFrom: any;
        tag: string;
        tagTo: string;
        tagFrom: any;
        type: string;
        amount: number;
        currency: any;
        status: string;
        updated: number;
        internal: number;
        fee: any;
    }>;
    parseTradingFee(fee: any, market?: any): {
        info: any;
        symbol: any;
        maker: number;
        taker: number;
    };
    fetchTradingFee(symbol: any, params?: {}): Promise<{
        info: any;
        symbol: any;
        maker: number;
        taker: number;
    }>;
    fetchTradingFees(params?: {}): Promise<{}>;
    futuresTransfer(code: any, amount: any, type: any, params?: {}): Promise<{
        info: any;
        id: string;
        timestamp: number;
        datetime: string;
        currency: any;
        amount: number;
        fromAccount: any;
        toAccount: any;
        status: string;
    }>;
    fetchFundingRate(symbol: any, params?: {}): Promise<{
        info: any;
        symbol: any;
        markPrice: number;
        indexPrice: number;
        interestRate: number;
        estimatedSettlePrice: number;
        timestamp: number;
        datetime: string;
        fundingRate: number;
        fundingTimestamp: number;
        fundingDatetime: string;
        nextFundingRate: any;
        nextFundingTimestamp: any;
        nextFundingDatetime: any;
        previousFundingRate: any;
        previousFundingTimestamp: any;
        previousFundingDatetime: any;
    }>;
    fetchFundingRateHistory(symbol?: string, since?: any, limit?: any, params?: {}): Promise<any>;
    fetchFundingRates(symbols?: string[], params?: {}): Promise<any>;
    parseFundingRate(contract: any, market?: any): {
        info: any;
        symbol: any;
        markPrice: number;
        indexPrice: number;
        interestRate: number;
        estimatedSettlePrice: number;
        timestamp: number;
        datetime: string;
        fundingRate: number;
        fundingTimestamp: number;
        fundingDatetime: string;
        nextFundingRate: any;
        nextFundingTimestamp: any;
        nextFundingDatetime: any;
        previousFundingRate: any;
        previousFundingTimestamp: any;
        previousFundingDatetime: any;
    };
    parseAccountPositions(account: any): any[];
    parseAccountPosition(position: any, market?: any): {
        info: any;
        id: any;
        symbol: string;
        timestamp: number;
        datetime: string;
        initialMargin: number;
        initialMarginPercentage: number;
        maintenanceMargin: number;
        maintenanceMarginPercentage: number;
        entryPrice: number;
        notional: number;
        leverage: number;
        unrealizedPnl: number;
        contracts: number;
        contractSize: any;
        marginRatio: any;
        liquidationPrice: any;
        markPrice: any;
        collateral: number;
        marginMode: any;
        side: any;
        hedged: boolean;
        percentage: any;
    };
    parsePositionRisk(position: any, market?: any): {
        info: any;
        id: any;
        symbol: string;
        contracts: number;
        contractSize: any;
        unrealizedPnl: number;
        leverage: number;
        liquidationPrice: number;
        collateral: number;
        notional: number;
        markPrice: number;
        entryPrice: number;
        timestamp: number;
        initialMargin: number;
        initialMarginPercentage: number;
        maintenanceMargin: number;
        maintenanceMarginPercentage: number;
        marginRatio: any;
        datetime: string;
        marginMode: string;
        marginType: string;
        side: any;
        hedged: boolean;
        percentage: any;
    };
    loadLeverageBrackets(reload?: boolean, params?: {}): Promise<any>;
    fetchLeverageTiers(symbols?: string[], params?: {}): Promise<{}>;
    parseMarketLeverageTiers(info: any, market: any): any[];
    fetchPositions(symbols?: string[], params?: {}): Promise<any>;
    fetchAccountPositions(symbols?: string[], params?: {}): Promise<any>;
    fetchPositionsRisk(symbols?: string[], params?: {}): Promise<any>;
    fetchFundingHistory(symbol?: string, since?: any, limit?: any, params?: {}): Promise<any>;
    setLeverage(leverage: any, symbol?: string, params?: {}): Promise<any>;
    setMarginMode(marginMode: any, symbol?: string, params?: {}): Promise<any>;
    setPositionMode(hedged: any, symbol?: string, params?: {}): Promise<any>;
    fetchSettlementHistory(symbol?: string, since?: any, limit?: any, params?: {}): Promise<any>;
    parseSettlement(settlement: any, market: any): {
        info: any;
        symbol: any;
        price: number;
        timestamp: number;
        datetime: string;
    };
    parseSettlements(settlements: any, market: any): any[];
    fetchLedger(code?: string, since?: any, limit?: any, params?: {}): Promise<any>;
    parseLedgerEntry(item: any, currency?: any): {
        id: string;
        direction: any;
        account: any;
        referenceAccount: any;
        referenceId: string;
        type: string;
        currency: any;
        amount: number;
        timestamp: number;
        datetime: string;
        before: any;
        after: any;
        status: any;
        fee: any;
        info: any;
    };
    parseLedgerEntryType(type: any): string;
    sign(path: any, api?: any, method?: string, params?: {}, headers?: any, body?: any): {
        url: any;
        method: string;
        body: any;
        headers: any;
    };
    handleErrors(code: any, reason: any, url: any, method: any, headers: any, body: any, response: any, requestHeaders: any, requestBody: any): any;
    calculateRateLimiterCost(api: any, method: any, path: any, params: any, config?: {}, context?: {}): any;
    request(path: any, api?: any, method?: string, params?: {}, headers?: any, body?: any, config?: {}, context?: {}): Promise<any>;
    modifyMarginHelper(symbol: any, amount: any, addOrReduce: any, params?: {}): Promise<any>;
    parseMarginModification(data: any, market?: any): {
        info: any;
        type: string;
        amount: number;
        code: any;
        symbol: any;
        status: string;
    };
    reduceMargin(symbol: any, amount: any, params?: {}): Promise<any>;
    addMargin(symbol: any, amount: any, params?: {}): Promise<any>;
    fetchBorrowRate(code: any, params?: {}): Promise<{
        currency: any;
        rate: number;
        period: number;
        timestamp: number;
        datetime: string;
        info: any;
    }>;
    fetchBorrowRateHistory(code: any, since?: any, limit?: any, params?: {}): Promise<any>;
    parseBorrowRateHistory(response: any, code: any, since: any, limit: any): any;
    parseBorrowRate(info: any, currency?: any): {
        currency: any;
        rate: number;
        period: number;
        timestamp: number;
        datetime: string;
        info: any;
    };
    createGiftCode(code: any, amount: any, params?: {}): Promise<{
        info: any;
        id: string;
        code: string;
        currency: any;
        amount: any;
    }>;
    redeemGiftCode(giftcardCode: any, params?: {}): Promise<any>;
    verifyGiftCode(id: any, params?: {}): Promise<any>;
    fetchBorrowInterest(code?: string, symbol?: string, since?: any, limit?: any, params?: {}): Promise<any>;
    parseBorrowInterest(info: any, market: any): {
        account: string;
        symbol: string;
        marginMode: string;
        currency: any;
        interest: number;
        interestRate: number;
        amountBorrowed: number;
        timestamp: number;
        datetime: string;
        info: any;
    };
    repayMargin(code: any, amount: any, symbol?: string, params?: {}): Promise<{
        id: number;
        currency: any;
        amount: any;
        symbol: any;
        timestamp: any;
        datetime: any;
        info: any;
    }>;
    borrowMargin(code: any, amount: any, symbol?: string, params?: {}): Promise<{
        id: number;
        currency: any;
        amount: any;
        symbol: any;
        timestamp: any;
        datetime: any;
        info: any;
    }>;
    parseMarginLoan(info: any, currency?: any): {
        id: number;
        currency: any;
        amount: any;
        symbol: any;
        timestamp: any;
        datetime: any;
        info: any;
    };
    fetchOpenInterestHistory(symbol: any, timeframe?: string, since?: any, limit?: any, params?: {}): Promise<any>;
    fetchOpenInterest(symbol: any, params?: {}): Promise<any>;
    parseOpenInterest(interest: any, market?: any): {
        symbol: any;
        baseVolume: number;
        quoteVolume: number;
        openInterestAmount: number;
        openInterestValue: number;
        timestamp: number;
        datetime: string;
        info: any;
    };
}
