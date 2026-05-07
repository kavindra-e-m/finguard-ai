package com.finguard.config;

import com.finguard.model.User;
import com.finguard.repository.UserRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.boot.CommandLineRunner;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Component;
import org.springframework.transaction.annotation.Transactional;

import java.math.BigDecimal;

/**
 * Data initializer to seed demo users on application startup.
 */
@Slf4j
@Component
@RequiredArgsConstructor
public class DataInitializer implements CommandLineRunner {
    
    private final UserRepository userRepository;
    private final PasswordEncoder passwordEncoder;
    
    @Override
    @Transactional
    public void run(String... args) throws Exception {
        log.info("Initializing database with demo data...");
        createDemoUser();
        log.info("Database initialization completed.");
    }
    
    /**
     * Create demo user if it doesn't exist.
     */
    private void createDemoUser() {
        String demoEmail = "demo@finguard.ai";
        
        // Check if demo user already exists
        if (userRepository.existsByEmail(demoEmail)) {
            log.info("Demo user already exists: {}", demoEmail);
            return;
        }
        
        // Create demo user
        User demoUser = new User();
        demoUser.setName("Demo User");
        demoUser.setEmail(demoEmail);
        demoUser.setPassword(passwordEncoder.encode("Demo@123"));
        demoUser.setMonthlyIncome(new BigDecimal("5000.00"));
        
        userRepository.save(demoUser);
        log.info("Demo user created successfully: {}", demoEmail);
    }
}
