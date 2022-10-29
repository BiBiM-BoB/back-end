import { IsJSON, IsNotEmpty, IsNumber, IsObject, IsString, MaxLength } from "class-validator";
export class CreateSecurityResultDto {
    
    @IsString()
    @IsNotEmpty()
    readonly data: string;
}