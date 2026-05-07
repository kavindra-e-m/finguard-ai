package com.finguard.service;

import com.finguard.config.MLServiceConfig;
import com.finguard.dto.response.*;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

import java.math.BigDecimal;
import java.util.*;

/**
 * Service for calling ML microservice.
 */
@Slf4j
@Service
@RequiredArgsConstructor
public class MLService {
    
    private final RestTemplate restTemplate;
    private final MLServiceConfig mlServiceConfig;
    
    /**
     * Predict future expenses.
     *
     * @param monthlyExpenses list of monthly expense data
     * @return expense prediction
     */
    public AnalyticsResponse.ExpensePrediction predictExpense(List<Map<String, Object>> monthlyExpenses) {
        log.info("Calling ML service for expense prediction");
        
        String url = mlServiceConfig.getMlServiceUrl() + "/ml/predict-expense";
        
        Map<String, Object> request = new HashMap<>();
        request.put("user_id", 1);
        request.put("monthly_expenses", monthlyExpenses);
        
        try {
            ResponseEntity<Map> response = restTemplate.postForEntity(url, request, Map.class);
            Map<String, Object> body = response.getBody();
            
            if (body != null) {
                return AnalyticsResponse.ExpensePrediction.builder()
                        .predictedNextMonth(new BigDecimal(body.get("predicted_next_month").toString()))
                        .confidenceLower(new BigDecimal(body.get("confidence_lower").toString()))
                        .confidenceUpper(new BigDecimal(body.get("confidence_upper").toString()))
                        .trend((String) body.get("trend"))
                        .forecast3Months(((List<Number>) body.get("forecast_3_months"))
                                .stream()
                                .map(n -> new BigDecimal(n.toString()))
                                .toList())
                        .build();
            }
        } catch (Exception e) {
            log.error("ML service call failed: {}", e.getMessage());
        }
        
        return null;
    }
    
    /**
     * Detect financial personality.
     *
     * @param features personality features
     * @return personality detection result
     */
    public AnalyticsResponse.PersonalityDetection detectPersonality(Map<String, Object> features) {
        log.info("Calling ML service for personality detection");
        
        String url = mlServiceConfig.getMlServiceUrl() + "/ml/detect-personality";
        
        try {
            ResponseEntity<Map> response = restTemplate.postForEntity(url, features, Map.class);
            Map<String, Object> body = response.getBody();
            
            if (body != null) {
                Map<String, Double> probs = new HashMap<>();
                Map<String, Object> probMap = (Map<String, Object>) body.get("probabilities");
                probMap.forEach((k, v) -> probs.put(k, ((Number) v).doubleValue()));
                
                return AnalyticsResponse.PersonalityDetection.builder()
                        .personalityType((String) body.get("personality_type"))
                        .confidence(((Number) body.get("confidence")).doubleValue())
                        .probabilities(probs)
                        .description((String) body.get("description"))
                        .build();
            }
        } catch (Exception e) {
            log.error("ML service call failed: {}", e.getMessage());
        }
        
        return null;
    }
    
    /**
     * Predict financial stress.
     *
     * @param features stress features
     * @return stress prediction result
     */
    public AnalyticsResponse.StressPrediction predictStress(Map<String, Object> features) {
        log.info("Calling ML service for stress prediction");
        
        String url = mlServiceConfig.getMlServiceUrl() + "/ml/predict-stress";
        
        try {
            ResponseEntity<Map> response = restTemplate.postForEntity(url, features, Map.class);
            Map<String, Object> body = response.getBody();
            
            if (body != null) {
                return AnalyticsResponse.StressPrediction.builder()
                        .riskScore(((Number) body.get("risk_score")).doubleValue())
                        .riskLabel((String) body.get("risk_label"))
                        .alerts((List<String>) body.get("alerts"))
                        .recommendations((List<String>) body.get("recommendations"))
                        .build();
            }
        } catch (Exception e) {
            log.error("ML service call failed: {}", e.getMessage());
        }
        
        return null;
    }
    
    /**
     * Optimize investment portfolio.
     *
     * @param request portfolio optimization request
     * @return optimization result
     */
    public PortfolioResponse.Optimization optimizePortfolio(Map<String, Object> request) {
        log.info("Calling ML service for portfolio optimization");
        
        String url = mlServiceConfig.getMlServiceUrl() + "/ml/optimize-portfolio";
        
        try {
            ResponseEntity<Map> response = restTemplate.postForEntity(url, request, Map.class);
            Map<String, Object> body = response.getBody();
            
            if (body != null) {
                Map<String, BigDecimal> amounts = new HashMap<>();
                Map<String, Object> amountMap = (Map<String, Object>) body.get("allocation_amounts");
                amountMap.forEach((k, v) -> amounts.put(k, new BigDecimal(v.toString())));
                
                return PortfolioResponse.Optimization.builder()
                        .weights((Map<String, Double>) body.get("weights"))
                        .allocationAmounts(amounts)
                        .expectedAnnualReturn(((Number) body.get("expected_annual_return")).doubleValue())
                        .annualVolatility(((Number) body.get("annual_volatility")).doubleValue())
                        .sharpeRatio(((Number) body.get("sharpe_ratio")).doubleValue())
                        .riskLabel((String) body.get("risk_label"))
                        .build();
            }
        } catch (Exception e) {
            log.error("ML service call failed: {}", e.getMessage());
        }
        
        return null;
    }
    
    /**
     * Calculate financial health score.
     *
     * @param features health features
     * @return financial health result
     */
    public FinancialHealthResponse calculateFinancialHealth(Map<String, Object> features) {
        log.info("Calling ML service for financial health score");
        
        String url = mlServiceConfig.getMlServiceUrl() + "/ml/financial-health-score";
        
        try {
            ResponseEntity<Map> response = restTemplate.postForEntity(url, features, Map.class);
            Map<String, Object> body = response.getBody();
            
            if (body != null) {
                Map<String, Integer> breakdown = new HashMap<>();
                Map<String, Object> breakdownMap = (Map<String, Object>) body.get("breakdown");
                breakdownMap.forEach((k, v) -> breakdown.put(k, ((Number) v).intValue()));
                
                return FinancialHealthResponse.builder()
                        .overallScore(((Number) body.get("overall_score")).intValue())
                        .grade((String) body.get("grade"))
                        .breakdown(breakdown)
                        .recommendations((List<String>) body.get("recommendations"))
                        .riskFactors((List<String>) body.get("risk_factors"))
                        .build();
            }
        } catch (Exception e) {
            log.error("ML service call failed: {}", e.getMessage());
        }
        
        return null;
    }
    
    /**
     * Detect anomalous expenses.
     *
     * @param expenses list of expenses
     * @return anomaly detection result
     */
    public AnalyticsResponse.AnomalyDetection detectAnomalies(List<Map<String, Object>> expenses) {
        log.info("Calling ML service for anomaly detection");
        
        String url = mlServiceConfig.getMlServiceUrl() + "/ml/detect-anomalies";
        
        Map<String, Object> request = new HashMap<>();
        request.put("expenses", expenses);
        
        try {
            ResponseEntity<Map> response = restTemplate.postForEntity(url, request, Map.class);
            Map<String, Object> body = response.getBody();
            
            if (body != null) {
                List<Map<String, Object>> anomalyList = (List<Map<String, Object>>) body.get("anomalies");
                List<AnalyticsResponse.AnomalyItem> anomalies = anomalyList.stream()
                        .map(a -> AnalyticsResponse.AnomalyItem.builder()
                                .expenseId(((Number) a.get("expense_id")).longValue())
                                .amount(new BigDecimal(a.get("amount").toString()))
                                .category((String) a.get("category"))
                                .anomalyScore(((Number) a.get("anomaly_score")).doubleValue())
                                .reason((String) a.get("reason"))
                                .build())
                        .toList();
                
                return AnalyticsResponse.AnomalyDetection.builder()
                        .anomalies(anomalies)
                        .totalAnomalies((Integer) body.get("total_anomalies"))
                        .totalTransactions((Integer) body.get("total_transactions"))
                        .build();
            }
        } catch (Exception e) {
            log.error("ML service call failed: {}", e.getMessage());
        }
        
        return null;
    }
}
