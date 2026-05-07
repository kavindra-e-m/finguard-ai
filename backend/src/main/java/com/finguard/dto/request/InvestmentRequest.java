package com.finguard.dto.request;

import com.finguard.model.Investment.InvestmentType;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Positive;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.math.BigDecimal;
import java.time.LocalDate;

/**
 * Request DTO for creating an investment.
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
public class InvestmentRequest {
    
    @NotNull(message = "Investment type is required")
    private InvestmentType investmentType;
    
    @NotNull(message = "Amount is required")
    @Positive(message = "Amount must be positive")
    private BigDecimal amount;
    
    @Positive(message = "Expected return must be positive")
    private BigDecimal expectedReturn;
    
    @NotNull(message = "Investment date is required")
    private LocalDate investmentDate;
}
