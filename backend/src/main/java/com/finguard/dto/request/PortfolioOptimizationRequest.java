package com.finguard.dto.request;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Positive;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.math.BigDecimal;

/**
 * Request DTO for portfolio optimization.
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
public class PortfolioOptimizationRequest {
    
    @NotBlank(message = "Risk tolerance is required")
    private String riskTolerance;
    
    @NotNull(message = "Available capital is required")
    @Positive(message = "Available capital must be positive")
    private BigDecimal availableCapital;
    
    @Positive(message = "Investment horizon must be positive")
    private Integer investmentHorizonYears = 5;
}
