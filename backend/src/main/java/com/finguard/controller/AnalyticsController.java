package com.finguard.controller;

import com.finguard.dto.response.AnalyticsResponse;
import com.finguard.dto.response.FinancialHealthResponse;
import com.finguard.security.UserPrincipal;
import com.finguard.service.AnalyticsService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.security.SecurityRequirement;
import io.swagger.v3.oas.annotations.tags.Tag;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

/**
 * Controller for analytics operations.
 */
@RestController
@RequestMapping("/api/analytics")
@RequiredArgsConstructor
@SecurityRequirement(name = "bearerAuth")
@Tag(name = "Analytics", description = "Financial analytics and ML predictions")
public class AnalyticsController {
    
    private final AnalyticsService analyticsService;
    
    /**
     * Predict future expenses.
     *
     * @param userPrincipal authenticated user
     * @return expense prediction
     */
    @GetMapping("/predict-expense")
    @Operation(summary = "Predict expenses", description = "Predict next month expenses using ML")
    public ResponseEntity<AnalyticsResponse.ExpensePrediction> predictExpense(
            @AuthenticationPrincipal UserPrincipal userPrincipal) {
        return ResponseEntity.ok(analyticsService.predictExpense(userPrincipal.getId()));
    }
    
    /**
     * Detect financial personality.
     *
     * @param userPrincipal authenticated user
     * @return personality detection result
     */
    @GetMapping("/personality")
    @Operation(summary = "Detect personality", description = "Detect financial personality type")
    public ResponseEntity<AnalyticsResponse.PersonalityDetection> detectPersonality(
            @AuthenticationPrincipal UserPrincipal userPrincipal) {
        return ResponseEntity.ok(analyticsService.detectPersonality(userPrincipal.getId()));
    }
    
    /**
     * Predict financial stress.
     *
     * @param userPrincipal authenticated user
     * @return stress prediction result
     */
    @GetMapping("/stress")
    @Operation(summary = "Predict stress", description = "Predict financial stress level")
    public ResponseEntity<AnalyticsResponse.StressPrediction> predictStress(
            @AuthenticationPrincipal UserPrincipal userPrincipal) {
        return ResponseEntity.ok(analyticsService.predictStress(userPrincipal.getId()));
    }
    
    /**
     * Calculate financial health score.
     *
     * @param userPrincipal authenticated user
     * @return financial health result
     */
    @GetMapping("/financial-health")
    @Operation(summary = "Financial health score", description = "Calculate comprehensive financial health score")
    public ResponseEntity<FinancialHealthResponse> calculateFinancialHealth(
            @AuthenticationPrincipal UserPrincipal userPrincipal) {
        return ResponseEntity.ok(analyticsService.calculateFinancialHealth(userPrincipal.getId()));
    }
    
    /**
     * Detect anomalous expenses.
     *
     * @param userPrincipal authenticated user
     * @return anomaly detection result
     */
    @GetMapping("/anomalies")
    @Operation(summary = "Detect anomalies", description = "Detect anomalous expense transactions")
    public ResponseEntity<AnalyticsResponse.AnomalyDetection> detectAnomalies(
            @AuthenticationPrincipal UserPrincipal userPrincipal) {
        return ResponseEntity.ok(analyticsService.detectAnomalies(userPrincipal.getId()));
    }
}
