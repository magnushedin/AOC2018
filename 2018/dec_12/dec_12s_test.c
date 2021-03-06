#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <limits.h>

#define MAX_POTS 45
#define PATTERNS 14

char pattern[14][6];

void add_dot_before(char *gen)
{
    char a, b;
    for (int i=(MAX_POTS-2); i>=0; i--) {
        gen[i+1] = gen[i];
    }
    gen[0] = '.';
}

void add_dot_after(char * curr_gen)
{
    char* nbr;
    
    nbr = strrchr(curr_gen, '#');
    nbr[1] = '.';
    nbr[2] = '.';
    nbr[3] = '.';
}

int strchrm(char gen[MAX_POTS], char token)
{
    for (int i=0; i<MAX_POTS; i++) {
        //printf("%c ", gen[i]);
        if (gen[i] == token) {
            //printf("i: %d\n", i);
            return i;
        }
    }
    return INT_MAX;
}

char calc_plant(int i, char *curr_gen)
{
    char tmp[5];

    strncpy(tmp, &curr_gen[i-2], 5);

    //printf("%d, tmp: %s\n", i, tmp);

    for (int i=0; i<PATTERNS; i++){
        if (strncmp(tmp, pattern[i], 5) == 0) {
            //printf("%d, tmp: %s, pattern: %s\n", i, tmp, pattern[i]);
            return '#';
        }
    }
    
    return '.';
}

void print_string(int gen, char* curr_gen)
{
    char spacer[2] = "";

    if (gen<10) strncpy(spacer, " ", 2); else strncpy(spacer, "", 2);
    printf("%s%d: %s\n", spacer, gen, curr_gen);
}


int calc_points(int min_index, char* curr_gen)
{
    int points = 0;
    for (int i=0; i<MAX_POTS; i++) {
        if (curr_gen[i] == '#') {
            points += (i+min_index);
            printf("%d: %d (%d)\n", i, i+min_index, points);
        }
    }
    return points;
}

int main(int argc, char *argv[])
{
    char curr_gen[MAX_POTS] = {'\0'};
    char next_gen[MAX_POTS] = {'\0'};
    char tmp[MAX_POTS] = {'\0'};
    int ng = 0;
    int points = 0;
    int min_index = 0;

    strncpy(pattern[0], "...##", 5);
    strncpy(pattern[1], "..#..", 5);
    strncpy(pattern[2], ".#...", 5);
    strncpy(pattern[3], ".#.#.", 5);
    strncpy(pattern[4], ".#.##", 5);
    strncpy(pattern[5], ".##..", 5);
    strncpy(pattern[6], ".####", 5);
    strncpy(pattern[7], "#.#.#", 5);
    strncpy(pattern[8], "#.###", 5);
    strncpy(pattern[9], "##.#.", 5);
    strncpy(pattern[10], "##.##", 5);
    strncpy(pattern[11], "###..", 5);
    strncpy(pattern[12], "###.#", 5);
    strncpy(pattern[13], "####.", 5);

    // Initial state
    strncpy(curr_gen, "#..#.#..##......###...###", 26);

    // Simulate each generation
    for (int gen=0; gen<=19; gen++) {

        // add dots before
        while (strchrm(curr_gen, '#') < 3) {
            add_dot_before(curr_gen);
            min_index--;
        }

        // add dots after
        add_dot_after(curr_gen);

        // print the string
        print_string(gen, curr_gen);

        // Calculate next generation
        strncpy(next_gen, "................................................................", MAX_POTS);
        
        for (int i=2; i<MAX_POTS; i++) {
            next_gen[i] = calc_plant(i, curr_gen);
        }

        strncpy(curr_gen, next_gen, MAX_POTS);

    }

    print_string(20, curr_gen);
    points = calc_points(min_index, curr_gen);

    printf("Points: %d, min_index: %d\n", points, min_index);
}