package com.finguard.security;

import com.finguard.model.User;
import com.fasterxml.jackson.annotation.JsonIgnore;
import lombok.AllArgsConstructor;
import lombok.Data;
import org.springframework.security.core.GrantedAuthority;
import org.springframework.security.core.authority.SimpleGrantedAuthority;
import org.springframework.security.core.userdetails.UserDetails;

import java.util.Collection;
import java.util.Collections;

/**
 * User principal for Spring Security authentication.
 */
@Data
@AllArgsConstructor
public class UserPrincipal implements UserDetails {
    
    private Long id;
    private String name;
    private String email;
    
    @JsonIgnore
    private String password;
    
    private Collection<? extends GrantedAuthority> authorities;
    
    /**
     * Create UserPrincipal from User entity.
     *
     * @param user the user entity
     * @return UserPrincipal
     */
    public static UserPrincipal create(User user) {
        return new UserPrincipal(
                user.getId(),
                user.getName(),
                user.getEmail(),
                user.getPassword(),
                Collections.singletonList(new SimpleGrantedAuthority("ROLE_USER"))
        );
    }
    
    @Override
    public String getUsername() {
        return email;
    }
    
    @Override
    public boolean isAccountNonExpired() {
        return true;
    }
    
    @Override
    public boolean isAccountNonLocked() {
        return true;
    }
    
    @Override
    public boolean isCredentialsNonExpired() {
        return true;
    }
    
    @Override
    public boolean isEnabled() {
        return true;
    }
}
