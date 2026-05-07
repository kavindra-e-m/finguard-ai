package com.finguard.repository;

import com.finguard.model.Investment;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.math.BigDecimal;
import java.util.List;

/**
 * Repository for Investment entity operations.
 */
@Repository
public interface InvestmentRepository extends JpaRepository<Investment, Long> {
    
    /**
     * Find all investments for a user.
     *
     * @param userId the user ID
     * @return list of investments
     */
    List<Investment> findByUserId(Long userId);
    
    /**
     * Find investments by type for a user.
     *
     * @param userId the user ID
     * @param investmentType the investment type
     * @return list of investments
     */
    List<Investment> findByUserIdAndInvestmentType(Long userId, Investment.InvestmentType investmentType);
    
    /**
     * Get total invested amount by user.
     *
     * @param userId the user ID
     * @return total amount
     */
    @Query("SELECT COALESCE(SUM(i.amount), 0) FROM Investment i WHERE i.user.id = :userId")
    BigDecimal getTotalInvestedByUser(@Param("userId") Long userId);
    
    /**
     * Get investment breakdown by type.
     *
     * @param userId the user ID
     * @return list of type and amount tuples
     */
    @Query("SELECT i.investmentType, SUM(i.amount) FROM Investment i WHERE i.user.id = :userId GROUP BY i.investmentType")
    List<Object[]> getInvestmentBreakdown(@Param("userId") Long userId);
}
