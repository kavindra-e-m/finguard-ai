package com.finguard.controller;

import com.finguard.dto.request.InvestmentRequest;
import com.finguard.dto.request.PortfolioOptimizationRequest;
import com.finguard.dto.response.PortfolioResponse;
import com.finguard.security.UserPrincipal;
import com.finguard.service.InvestmentService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.security.SecurityRequirement;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.web.bind.annotation.*;

import java.util.List;

/**
 * Controller for investment operations.
 */
@RestController
@RequestMapping("/api/investments")
@RequiredArgsConstructor
@SecurityRequirement(name = "bearerAuth")
@Tag(name = "Investments", description = "Investment management endpoints")
public class InvestmentController {
    
    private final InvestmentService investmentService;
    
    /**
     * Create a new investment.
     *
     * @param userPrincipal authenticated user
     * @param request investment request
     * @return created investment
     */
    @PostMapping
    @Operation(summary = "Create investment", description = "Add a new investment record")
    public ResponseEntity<PortfolioResponse.Investment> createInvestment(
            @AuthenticationPrincipal UserPrincipal userPrincipal,
            @Valid @RequestBody InvestmentRequest request) {
        return ResponseEntity.status(HttpStatus.CREATED)
                .body(investmentService.createInvestment(userPrincipal.getId(), request));
    }
    
    /**
     * Get all investments for the authenticated user.
     *
     * @param userPrincipal authenticated user
     * @return list of investments
     */
    @GetMapping
    @Operation(summary = "Get investments", description = "Get all user investments")
    public ResponseEntity<List<PortfolioResponse.Investment>> getInvestments(
            @AuthenticationPrincipal UserPrincipal userPrincipal) {
        return ResponseEntity.ok(investmentService.getUserInvestments(userPrincipal.getId()));
    }
    
    /**
     * Get portfolio summary.
     *
     * @param userPrincipal authenticated user
     * @return portfolio summary
     */
    @GetMapping("/summary")
    @Operation(summary = "Get portfolio summary", description = "Get portfolio summary and statistics")
    public ResponseEntity<PortfolioResponse.Summary> getPortfolioSummary(
            @AuthenticationPrincipal UserPrincipal userPrincipal) {
        return ResponseEntity.ok(investmentService.getPortfolioSummary(userPrincipal.getId()));
    }
    
    /**
     * Optimize portfolio.
     *
     * @param userPrincipal authenticated user
     * @param request optimization request
     * @return optimization result
     */
    @PostMapping("/optimize")
    @Operation(summary = "Optimize portfolio", description = "Get optimal portfolio allocation using ML")
    public ResponseEntity<PortfolioResponse.Optimization> optimizePortfolio(
            @AuthenticationPrincipal UserPrincipal userPrincipal,
            @Valid @RequestBody PortfolioOptimizationRequest request) {
        return ResponseEntity.ok(investmentService.optimizePortfolio(userPrincipal.getId(), request));
    }
}
