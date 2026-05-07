package com.finguard.model;

import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.hibernate.annotations.CreationTimestamp;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.time.LocalDateTime;

/**
 * Investment entity representing a user's investment record.
 */
@Entity
@Table(name = "investments")
@Data
@NoArgsConstructor
@AllArgsConstructor
public class Investment {
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "user_id", nullable = false)
    private User user;
    
    @Column(name = "investment_type", nullable = false, length = 50)
    @Enumerated(EnumType.STRING)
    private InvestmentType investmentType;
    
    @Column(nullable = false, precision = 12, scale = 2)
    private BigDecimal amount;
    
    @Column(name = "expected_return", precision = 12, scale = 4)
    private BigDecimal expectedReturn;
    
    @Column(name = "investment_date", nullable = false)
    private LocalDate investmentDate;
    
    @CreationTimestamp
    @Column(name = "created_at", updatable = false)
    private LocalDateTime createdAt;
    
    /**
     * Constructor for creating a new investment.
     */
    public Investment(User user, InvestmentType investmentType, BigDecimal amount,
                      BigDecimal expectedReturn, LocalDate investmentDate) {
        this.user = user;
        this.investmentType = investmentType;
        this.amount = amount;
        this.expectedReturn = expectedReturn;
        this.investmentDate = investmentDate;
    }
    
    /**
     * Investment types.
     */
    public enum InvestmentType {
        STOCKS,
        MUTUAL_FUNDS,
        BONDS,
        CRYPTO,
        GOLD,
        FD
    }
}
