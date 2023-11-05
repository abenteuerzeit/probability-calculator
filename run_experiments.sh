#!/bin/bash

# Function to print a separator line based on the terminal width
print_separator() {
    local width=$(tput cols)
    local separator=$(printf '%*s' "$width" '' | tr ' ' '-')
    echo -e "\033[1;37m$separator\033[0m"
}

print_box() {
    local text="$1"
    local -r terminal_width=$(tput cols)
    local -r padding=2
    local -r border_char='-'
    local emoji_multiplier=2  # Width multiplier for emojis

    # Count the number of emoji characters
    local emoji_count=$(grep -o -e "🟦" -e "🟥" -e "🟩" -e "🟨" -e "⬛" -e "⬜" -e "🟧" <<< "$text" | wc -l)

    # Adjust for emoji width by removing emoji characters from the string length calculation
    local adjusted_text_length=$((${#text} - emoji_count))

    # Check if the text length exceeds the available space and shorten it if necessary
    if [ $((adjusted_text_length + emoji_count * emoji_multiplier + padding * 2 + 2)) -gt $terminal_width ]; then
        # Shorten the text to fit in the box with padding
        local max_text_length=$(($terminal_width - padding * 2 - emoji_count * emoji_multiplier - 2))
        text="${text:0:$max_text_length}"
    fi

    # Recalculate the full length for the box including emojis
    local full_length=$((${#text} + emoji_count * (emoji_multiplier - 1) + padding * 2))

    # Box top border
    echo -en "\033[1;44m"  # Blue background
    echo -n '+'
    for ((i = 0; i < full_length; i++)); do echo -n "$border_char"; done
    echo -n '+'
    echo -e "\033[0m"

    # Box text line
    echo -en "\033[1;44m"  # Blue background
    printf "|%*s%s%*s|" $padding " " "$text" $padding " "
    echo -e "\033[0m"

    # Box bottom border
    echo -en "\033[1;44m"  # Blue background
    echo -n '+'
    for ((i = 0; i < full_length; i++)); do echo -n "$border_char"; done
    echo -n '+'
    echo -e "\033[0m"
}





print_header() {
    echo -e "\n\033[1;34m$1\033[0m"
}

generate_random_hat() {
    colors=("blue" "red" "green" "yellow" "black" "white" "orange")
    hat_config=""
    for color in "${colors[@]}"; do
        count=$(($RANDOM % 10 + 1))
        hat_config+="$color=$count "
    done
    echo "$hat_config"
}

print_result() {
    local result=$1
    local padding="  "
    echo -e "${padding}Result: $result\n"
}

num_experiments=${1:-10}

total_successes=0

for i in $(seq 1 $num_experiments); do
    hat_config=$(generate_random_hat)
    expected_config=$(generate_random_hat)
    num_balls_drawn=$(($RANDOM % 10 + 1))

    print_box " Experiment $i: Hat: $hat_config | Expected: $expected_config | Draw: $num_balls_drawn "

    result=$(python main.py --hat "$hat_config" --expected "$expected_config" --draw "$num_balls_drawn" --experiments 1)

    if echo "$result" | grep -q "Total Successes: 1/1"; then
        ((total_successes++))
    fi

    print_result "$result" | sed 's/%/%%/g'
    print_separator
done

# Summary of experiments
print_header "Total Successes: $total_successes/$num_experiments"
print_separator
