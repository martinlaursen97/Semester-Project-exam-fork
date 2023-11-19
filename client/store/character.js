import { defineStore } from 'pinia'

export const useCharacterStore = defineStore('character', () => {
    const character = ref({})
    const setCharacter = (char) => {
        character.value = char
        localStorage.setItem('character', JSON.stringify(char))
    }
    const getCharacter = () => {
        if (typeof window === "undefined") return null;
        const storedCharacter = JSON.parse(localStorage.getItem('character'))
        return storedCharacter
    }
    return {
        character,
        setCharacter,
        getCharacter
    }
})