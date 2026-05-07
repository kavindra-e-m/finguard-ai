package com.finguard.service;

import com.finguard.dto.request.InvestmentRequest;
import com.finguard.dto.request.PortfolioOptimizationRequest;
import com.finguard.dto.response.PortfolioResponse;
import com.finguard.model.Investment;
import com.finguard.model.User;
import com.finguard.repository.InvestmentRepository;
import com.finguard.repository.UserRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.math.BigDecimal;
import java.math.RoundingMode;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

/**
 * Service for investment operations.
 */
@Slf4j
@Service
@RequiredArgsConstructor
public class InvestmentService {
    
    private final InvestmentRepository investmentRepository;
    private final UserRepository userRepository;
    private final MLService mlService;
    
    /**
     * Create a new investment.
     *
     * @param userId the user ID
     * @param request investment request
     * @return created investment response
     */
    @Transactional
    public PortfolioResponse.Investment createInvestment(Long userId, InvestmentRequest request) {
        log.info("Creating investment for user: {}", userId);
        
        User user = userRepository.findById(userId)
                .orElseThrow(() -> new RuntimeException("User not found"));
        
        Investment investment = new Investment();
        investment.setUser(user);
        investment.setInvestmentType(request.getInvestmentType());
        investment.setAmount(request.getAmount());
        investment.setExpectedReturn(request.getExpectedReturn());
        investment.setInvestmentDate(request.getInvestmentDate());
        
        investmentRepository.save(investment);
        
        return mapToResponse(investment);
    }
    
    /**
     * Get all investments for a user.
     *
     * @param userId the user ID
     * @return list of investment responses
     */
    public List<PortfolioResponse.Investment> getUserInvestments(Long userId) {
        return investmentRepository.findByUserId(userId).stream()
                .map(this::mapToResponse)
                .collect(Collectors.toList());
    }
    
    /**
     * Get portfolio summary for a user.
     *
     * @param userId the user ID
     * @return portfolio summary
     */
    public PortfolioResponse.Summary getPortfolioSummary(Long userId) {
        List<Investment> investments = investmentRepository.findByUserId(userId);
        
        BigDecimal totalInvested = investments.stream()
                .map(Investment::getAmount)
                .reduce(BigDecimal.ZERO, BigDecimal::add);
        
        // Calculate current value based on expected returns
        BigDecimal totalCurrentValue = investments.stream()
                .map(inv -> {
                    if (inv.getExpectedReturn() != null) {
                        return inv.getAmount().multiply(
                                BigDecimal.ONE.add(inv.getExpectedReturn()));
                    }
                    return inv.getAmount();
                })
                .reduce(BigDecimal.ZERO, BigDecimal::add);
        
        BigDecimal totalReturn = totalCurrentValue.subtract(totalInvested);
        double returnPercentage = totalInvested.compareTo(BigDecimal.ZERO) > 0 ?
                totalReturn.multiply(BigDecimal.valueOf(100))
                        .divide(totalInvested, 2, RoundingMode.HALF_UP)
                        .doubleValue() : 0;
        
        // Get asset allocation
        List<Object[]> breakdown = investmentRepository.getInvestmentBreakdown(userId);
        Map<String, BigDecimal> assetAllocation = new HashMap<>();
        
        for (Object[] obj : breakdown) {
            String type = obj[0].toString();
            BigDecimal amount = (BigDecimal) obj[1];
            assetAllocation.put(type, amount);
        }
        
        return PortfolioResponse.Summary.builder()
                .totalInvested(totalInvested)
                .totalCurrentValue(totalCurrentValue)
                .totalReturn(totalReturn)
                .returnPercentage(returnPercentage)
                .assetAllocation(assetAllocation)
                .investments(investments.stream().map(this::mapToResponse).collect(Collectors.toList()))
                .build();
    }
    
    /**
     * Optimize portfolio for a user.
     *
     * @param userId the user ID
     * @param request optimization request
     * @return optimization result
     */
    public PortfolioResponse.Optimization optimizePortfolio(Long userId, PortfolioOptimizationRequest request) {
        log.info("Optimizing portfolio for user: {}", userId);
        
        Map<String, Object> mlRequest = new HashMap<>();
        mlRequest.put("risk_tolerance", request.getRiskTolerance());
        mlRequest.put("available_capital", request.getAvailableCapital().doubleValue());
        mlRequest.put("investment_horizon_years", request.getInvestmentHorizonYears());
        
        return mlService.optimizePortfolio(mlRequest);
    }
    
    /**
     * Map Investment entity to InvestmentResponse DTO.
     *
     * @param investment the investment entity
     * @return InvestmentResponse
     */
    private PortfolioResponse.Investment mapToResponse(Investment investment) {
        return PortfolioResponse.Investment.builder()
                .id(investment.getId())
                .investmentType(investment.getInvestmentType().toString())
                .amount(investment.getAmount())
                .expectedReturn(investment.getExpectedReturn() != null ?
                        investment.getExpectedReturn().doubleValue() : null)
                .investmentDate(investment.getInvestmentDate())
                .build();
    }
}
