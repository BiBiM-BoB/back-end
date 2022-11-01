import { IsJSON, IsNotEmpty, IsNumber, IsObject, IsString, MaxLength } from "class-validator";
export class ToolDto {

    @IsNotEmpty()
    @IsString()
    readonly id: number;
    
    @IsNotEmpty()
    @IsString()
    readonly name: string;

    @IsNotEmpty()
    readonly stage: string;

    @IsNotEmpty()
    readonly createAt: Date;
    
    @IsNotEmpty()
    readonly updateAt: Date;

    @IsNotEmpty()
    readonly deleteAt: Date;
}