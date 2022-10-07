import { IsNotEmpty, IsNumber, IsString, MaxLength } from "class-validator";
export class CreateSecurityResultDto {
    @IsString()
    @MaxLength(30)
    @IsNotEmpty()
    readonly name: string;

    @IsNumber()
    @IsNotEmpty()
    readonly age: number;
    
    @IsNumber()
    @IsNotEmpty()
    readonly location: string;
}