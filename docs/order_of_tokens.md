# Permissible ordering of token types in a PGN file
## Types of tokens
* M: Movetext
* N: NAG
* C: Comment
* (: Begin variation
* ): Close variation

# Constraints

* !. None of the following may occur before the first movetext token:
    * (: Begin variation
    * ): Close variation
    * N: NAG
    * Corollary: The initial token of the game must be either (a) a comment (C) token or (b) a movetext (M) token.
* 2. Any NAG token is optional, but if present must immediately follow a movetext (M) token.
* 3. Any Close-variation tag (“)”) may occur only when there is a positive imbalance of Begin-variation tags less Close-variation tags
* 6. An Open-variation (“(”) token
    * MAY immediately follow a tag from the following group:
        * Movetext (M)
        * NAG (N)
        * A comment tag (“C”). 
        * A Close-variation tag (“)”)
    * may NOT immediately follow a tag from the following group:
        * An Open-variation (“(”) token
* 4. A comment tag
    * MAY immediately follow a tag from the following group:
        * Movetext (M)
        * NAG (N)
        * Begin-variation tag (“(”)
    * may NOT immediately follow any tag from the following group:
        * A Close-variation tag (“)”)
        * A comment tag (“C”). (This would be well defined, however. You could just combine the comments.)
