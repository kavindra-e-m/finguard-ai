package com.finguard.service;

import com.finguard.dto.request.LoginRequest;
import com.finguard.dto.request.RegisterRequest;
import com.finguard.dto.response.AuthResponse;
import com.finguard.model.User;
import com.finguard.repository.UserRepository;
import com.finguard.security.JwtTokenProvider;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.Authentication;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.math.BigDecimal;

/**
 * Service for authentication operations.
 */
@Slf4j
@Service
@RequiredArgsConstructor
public class AuthService {
    
    private final UserRepository userRepository;
    private final PasswordEncoder passwordEncoder;
    private final JwtTokenProvider tokenProvider;
    private final AuthenticationManager authenticationManager;
    
    /**
     * Register a new user.
     *
     * @param request registration request
     * @return authentication response with token
     */
    @Transactional
    public AuthResponse register(RegisterRequest request) {
        log.info("Registering new user: {}", request.getEmail());
        
        // Check if email exists
        if (userRepository.existsByEmail(request.getEmail())) {
            throw new RuntimeException("Email already registered");
        }
        
        // Create new user
        User user = new User();
        user.setName(request.getName());
        user.setEmail(request.getEmail());
        user.setPassword(passwordEncoder.encode(request.getPassword()));
        user.setMonthlyIncome(request.getMonthlyIncome() != null ? 
                request.getMonthlyIncome() : BigDecimal.ZERO);
        
        userRepository.save(user);
        
        // Generate token
        String token = tokenProvider.generateToken(
                user.getId(), user.getEmail(), user.getName()
        );
        
        log.info("User registered successfully: {}", user.getEmail());
        
        return buildAuthResponse(token, user);
    }
    
    /**
     * Authenticate user login.
     *
     * @param request login request
     * @return authentication response with token
     */
    public AuthResponse login(LoginRequest request) {
        log.info("User login attempt: {}", request.getEmail());
        
        Authentication authentication = authenticationManager.authenticate(
                new UsernamePasswordAuthenticationToken(
                        request.getEmail(),
                        request.getPassword()
                )
        );
        
        String token = tokenProvider.generateToken(authentication);
        
        User user = userRepository.findByEmail(request.getEmail())
                .orElseThrow(() -> new RuntimeException("User not found"));
        
        log.info("User logged in successfully: {}", user.getEmail());
        
        return buildAuthResponse(token, user);
    }
    
    /**
     * Build authentication response.
     *
     * @param token JWT token
     * @param user user entity
     * @return AuthResponse
     */
    private AuthResponse buildAuthResponse(String token, User user) {
        return AuthResponse.builder()
                .token(token)
                .user(AuthResponse.UserInfo.builder()
                        .id(user.getId())
                        .name(user.getName())
                        .email(user.getEmail())
                        .monthlyIncome(user.getMonthlyIncome() != null ? 
                                user.getMonthlyIncome().toString() : "0")
                        .build())
                .build();
    }
}
